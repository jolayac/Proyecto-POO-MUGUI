# viewmodel/authentication_vm.py
from Model.firebase_authentication import FirebaseAuthentication
from typing import Callable, Optional
import os
import webbrowser
from urllib.parse import urlparse, parse_qs, urlencode
import http.server
import socketserver
import threading
import secrets
import base64
import hashlib
import requests
from dotenv import load_dotenv


class AuthenticationViewModel:
    """ViewModel que conecta las vistas con FirebaseAuthentication"""

    def __init__(self):
        load_dotenv()
        self.auth_service = FirebaseAuthentication()
        self.on_auth_success: Optional[Callable[[dict], None]] = None
        self.on_auth_error: Optional[Callable[[str], None]] = None

        # Estado para OAuth
        self._code_verifier: Optional[str] = None
        self._state: Optional[str] = None
        self._server: Optional[socketserver.TCPServer] = None
        self._server_thread: Optional[threading.Thread] = None

    def sign_in_with_google(self, id_token: str):
        """Llamado desde la vista al hacer clic en Google (con id_token)"""
        result = self.auth_service.sign_in_with_google(id_token)

        if result["success"]:
            if self.on_auth_success:
                self.on_auth_success(result["user"])
        else:
            error = result["error"]
            if "Ya existe una cuenta" in error:
                if self.on_auth_error:
                    self.on_auth_error("Cuenta ya existe. Por favor, inicia sesión.")
            else:
                if self.on_auth_error:
                    self.on_auth_error(error)

    def get_current_user(self):
        return self.auth_service.get_current_user()

    def sign_out(self):
        self.auth_service.sign_out()

    def _generate_pkce(self):
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(64)).decode('utf-8').rstrip("=")
        digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(digest).decode('utf-8').rstrip("=")
        return code_verifier, code_challenge

    def start_google_auth(self, mode: str = "signin"):
        client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
        if not client_id:
            if self.on_auth_error:
                self.on_auth_error("Falta GOOGLE_OAUTH_CLIENT_ID en .env")
            return

        # Generar PKCE y state
        self._code_verifier, code_challenge = self._generate_pkce()
        self._state = secrets.token_urlsafe(16)

        port = int(os.getenv("GOOGLE_OAUTH_REDIRECT_PORT", "8000"))
        redirect_uri = f"http://localhost:{port}/callback"

        # Handler interno que tiene acceso a self
        class OAuthHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urlparse(self.path)
                if parsed.path != "/callback":
                    self.send_response(404)
                    self.end_headers()
                    return

                qs = parse_qs(parsed.query)
                code = qs.get("code", [None])[0]
                state = qs.get("state", [None])[0]
                error = qs.get("error", [None])[0]

                if error:
                    self._send_error(f"Error de Google: {error}")
                    return

                if not code or not state or state != self.server.viewmodel._state:
                    self._send_error("Estado inválido o código faltante")
                    return

                try:
                    token_data = {
                        "client_id": client_id,
                        "code": code,
                        "code_verifier": self.server.viewmodel._code_verifier,
                        "grant_type": "authorization_code",
                        "redirect_uri": redirect_uri,
                    }
                    response = requests.post("https://oauth2.googleapis.com/token", data=token_data)
                    response.raise_for_status()
                    token_json = response.json()

                    id_token = token_json.get("id_token")
                    if not id_token:
                        self._send_error("No se recibió id_token")
                        return

                    # Éxito: cerrar servidor y notificar
                    self._send_success()
                    threading.Thread(
                        target=self._complete_auth,
                        args=(id_token,),
                        daemon=True
                    ).start()

                except requests.RequestException as e:
                    self._send_error(f"Error al obtener token: {str(e)}")
                except Exception as e:
                    self._send_error(f"Error interno: {str(e)}")

            def _send_success(self):
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                <h3>Autenticaci&oacute;n completada</h3>
                <p>Puedes cerrar esta ventana.</p>
                <script>window.close();</script>
                """)

            def _send_error(self, message: str):
                if self.server.viewmodel.on_auth_error:
                    self.server.viewmodel.on_auth_error(message)
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f"Error: {message}".encode())

            def log_message(self, format, *args):
                return  # Silenciar logs

        # Configurar servidor con referencia al viewmodel
        try:
            self._server = socketserver.TCPServer(("127.0.0.1", port), OAuthHandler)
            self._server.viewmodel = self  # Inyección para acceso desde handler
        except OSError as e:
            if "Address already in use" in str(e):
                if self.on_auth_error:
                    self.on_auth_error(f"Puerto {port} ocupado. Cambia GOOGLE_OAUTH_REDIRECT_PORT.")
            else:
                if self.on_auth_error:
                    self.on_auth_error(f"Error al iniciar servidor: {str(e)}")
            return

        # Iniciar servidor en hilo
        self._server_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._server_thread.start()

        # Construir URL de autorización
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": self._state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "prompt": "consent",
            "access_type": "offline",
        }
        auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
        webbrowser.open(auth_url)

    def _complete_auth(self, id_token: str):
        """Ejecuta la autenticación con Firebase después del callback"""
        try:
            result = self.auth_service.sign_in_with_google(id_token)
            if result["success"]:
                if self.on_auth_success:
                    self.on_auth_success(result["user"])
            else:
                if self.on_auth_error:
                    self.on_auth_error(result["error"])
        finally:
            # Siempre cerrar el servidor
            if self._server:
                self._server.shutdown()
                self._server.server_close()
                self._server = None
            self._code_verifier = None
            self._state = None