# model/firebase_admin.py
import pyrebase
import requests
import os
from typing import Optional, Dict
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de Firebase (sin cambios)
firebase_config = {
    "apiKey": "AIzaSyCTI5_fE9Y-lOXu6aUSG23vZUD-19rwS1o",
    "authDomain": "proyecto-poo-mugui.firebaseapp.com",
    "databaseURL": "https://proyecto-poo-mugui-default-rtdb.firebaseio.com",
    "projectId": "proyecto-poo-mugui",
    "storageBucket": "proyecto-poo-mugui.firebasestorage.app",
    "messagingSenderId": "945352912383",
    "appId": "1:945352912383:web:299d8b1e90a2bb4b3f0bca",
    "measurementId": "G-490V0WW1N2"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()  # Instancia para RTDB


class FirebaseAdmin:
    """Clase que maneja autenticación y RTDB con Pyrebase.
    Mantiene la funcionalidad de autenticación original y agrega métodos para RTDB."""

    def __init__(self):
        self.current_user = None  # Guardará el usuario autenticado
        # Cargar Client ID y Secret desde variables de entorno (.env)
        self.google_client_id = os.getenv("client_id", "")
        self.google_client_secret = os.getenv("client_secret", "")

    # --- Métodos de Autenticación (sin cambios, pero ahora usan los nuevos creds) ---

    def get_google_auth_url(self) -> str:
        """Genera URL completa con response_type=code para OAuth flow en desktop.
        @return: str – URL para abrir en navegador (formato: https://accounts.google.com/o/oauth2/v2/auth?client_id=...&response_type=code&...).
        Alternativa: Usar google-auth-oauthlib para generar URL con más scopes automáticos."""
        return (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={self.google_client_id}"  # Usa el nuevo Client ID
            f"&redirect_uri=urn:ietf:wg:oauth:2.0:oob"
            f"&response_type=code"
            f"&scope=email%20profile%20openid"
        )

    def exchange_code_for_id_token(self, code: str) -> Dict:
        """Intercambia el 'code' obtenido de Google por un id_token válido.
        @param code: str – Código copiado de la página de Google (largo, como '4/0AX4...').
        @return: Dict – {'success': True, 'id_token': 'eyJ...'} o {'success': False, 'error': 'msg'}.
        Alternativa: Usar la lib google-auth para manejo automático de tokens (pip install google-auth)."""
        url = "https://oauth2.googleapis.com/token"  # Endpoint fijo de Google para token exchange
        data = {
            "code": code,  # El código temporal de autorización
            "client_id": self.google_client_id,  # Nuevo Client ID
            "client_secret": self.google_client_secret,  # Nuevo Secret
            # URI para desktop (out-of-band)
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
            "grant_type": "authorization_code"  # Tipo de grant fijo para este flujo
        }
        r = requests.post(url, data=data)  # POST request a Google
        if r.status_code != 200:  # Si no es OK (ej. 401 por client deleted)
            error_desc = r.json().get("error_description",
                                      "Error desconocido en intercambio de código")
            # Devuelve error legible
            return {"success": False, "error": error_desc}
        tokens = r.json()  # Parsea respuesta JSON de Google
        id_token = tokens.get("id_token")  # Extrae el JWT token
        if not id_token:
            return {"success": False, "error": "No se recibió id_token de Google"}
        return {"success": True, "id_token": id_token}

    def sign_in_with_google(self, id_token: str) -> Dict:
        """Inicia sesión o crea cuenta con Google usando el id_token.
        @param id_token: str – JWT de Google.
        @return: Dict – {'success': True, 'user': {...}} o {'success': False, 'error': 'msg'}.
        Alternativa: Usar pyrebase.auth.sign_in_with_id_token() directamente si el flujo es simple."""
        try:
            api_key = firebase_config["apiKey"]  # Tu API key de Firebase
            # Endpoint de Firebase para federated login
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={api_key}"
            payload = {  # Cuerpo JSON para el POST
                # Token + proveedor
                "postBody": f"id_token={id_token}&providerId=google.com",
                # URI para desktop (puede ser cualquier cosa válida)
                "requestUri": "http://localhost",
                "returnSecureToken": True,  # Devuelve token de sesión de Firebase
                "returnIdpCredential": True  # Devuelve credenciales de Google
            }
            r = requests.post(url, json=payload)  # Envía a Firebase
            if r.ok:  # Si 200 OK
                data = r.json()  # Parsea respuesta
                self.current_user = data  # Guarda en instancia
                return {"success": True, "user": data}
            else:  # Manejo de errores (ej. EMAIL_EXISTS)
                error = r.json().get("error", {})
                error_msg = error.get("message", r.text)
                if "EMAIL_EXISTS" in error_msg:
                    return {"success": False, "error": "Ya existe una cuenta con este correo. Inicia sesión en lugar de registrarte."}
                elif "INVALID_IDP_RESPONSE" in error_msg:
                    return {"success": False, "error": "Respuesta inválida de Google. Verifica el id_token."}
                else:
                    return {"success": False, "error": f"Error de Firebase: {error_msg}"}
        except Exception as e:
            return {"success": False, "error": f"Excepción en sign_in: {str(e)}"}

    def get_current_user(self) -> Optional[Dict]:
        """Devuelve el usuario actual si está logueado.
        @return: Optional[Dict] – Datos del usuario o None.
        Alternativa: Usar Firebase Auth SDK para refresh token automático."""
        return self.current_user

    def sign_out(self):
        """Cierra sesión borrando el usuario actual.
        Alternativa: Llamar auth.sign_out() de Pyrebase para limpieza completa."""
        self.current_user = None

    # --- Métodos para RTDB (sin cambios, ya que el problema es solo en Auth) ---

    def save_user_config(self, uid: str, config: dict) -> bool:
        """Guarda un JSON de configuración bajo /users/<UID>/config.
        @param uid: str – UID de Firebase.
        @param config: dict – Ej. {'theme': 'dark'}.
        @return: bool – True si éxito.
        Alternativa: Usar db.child().transaction() para updates atómicos."""
        try:
            ref = db.child("users").child(uid).child("config")
            ref.set(config)  # Set sobrescribe el nodo
            return True
        except Exception as e:
            print(f"Error guardando config en RTDB: {e}")
            return False

    def load_user_config(self, uid: str) -> dict:
        """Carga el JSON de configuración de /users/<UID>/config.
        @param uid: str – UID.
        @return: dict – Config o {} si no existe.
        Alternativa: db.stream() para listeners en tiempo real."""
        try:
            snapshot = db.child("users").child(
                uid).child("config").get()  # GET snapshot
            return snapshot or {}  # Val() implícito en Pyrebase
        except Exception as e:
            print(f"Error cargando config de RTDB: {e}")
            return {}

    def update_user_config(self, uid: str, updates: dict) -> bool:
        """Actualiza campos específicos en /users/<UID>/config.
        @param uid: str – UID.
        @param updates: dict – Ej. {'theme': 'light'}.
        @return: bool – True si éxito.
        Alternativa: db.child().push() para agregar items únicos."""
        try:
            ref = db.child("users").child(uid).child("config")
            ref.update(updates)  # Update mergea campos
            return True
        except Exception as e:
            print(f"Error actualizando config en RTDB: {e}")
            return False
