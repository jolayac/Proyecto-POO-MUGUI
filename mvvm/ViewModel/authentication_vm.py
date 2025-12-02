# viewmodel/authentication_vm.py
import json
import os
import webbrowser
import threading
from typing import Callable, Optional, Dict
from mvvm.Model.firebase_admin import FirebaseAdmin


class AuthenticationViewModel:
    """ViewModel que maneja autenticación con Google Firebase.
    Conecta la vista con FirebaseAdmin y gestiona estado de sesión."""

    def __init__(self):
        self.admin_service = FirebaseAdmin()
        self.current_user: Optional[Dict] = None
        self.is_logged_in = False
        self.session_file = "user_session.json"  # Archivo para persistencia

        # Callbacks
        self.on_auth_success: Callable[[dict], None] = None
        self.on_auth_error: Callable[[str], None] = None
        self.on_logout_success: Callable[[], None] = None
        self.on_session_loaded: Callable[[dict], None] = None

        # Cargar sesión si existe
        self.load_session_from_file()

    def start_google_signin(self) -> str:
        """Genera URL de autenticación con Google y la abre en navegador.
        @return: URL para autenticación."""
        url = self.admin_service.get_google_auth_url()

        # Abrir navegador automáticamente
        try:
            webbrowser.open(url)
        except Exception as e:
            if self.on_auth_error:
                self.on_auth_error(f"No se pudo abrir navegador: {str(e)}")

        return url

    def process_google_code(self, code: str):
        """Procesa el código de autorización de Google en un thread separado.
        @param code: Código obtenido de Google."""
        # Ejecutar en thread separado para no bloquear UI
        thread = threading.Thread(
            target=self._process_code_async, args=(code,), daemon=True)
        thread.start()

    def _process_code_async(self, code: str):
        """Procesamiento asincrónico del código de Google."""
        try:
            # Intercambiar código por id_token
            exchange = self.admin_service.exchange_code_for_id_token(code)
            if not exchange["success"]:
                if self.on_auth_error:
                    self.on_auth_error(exchange["error"])
                return

            # Iniciar sesión con el id_token
            id_token = exchange["id_token"]
            result = self.admin_service.sign_in_with_google(id_token)

            if result["success"]:
                user = result["user"]
                uid = user.get("localId")

                if uid:
                    # Guardar usuario
                    self.current_user = user
                    self.is_logged_in = True

                    # Guardar sesión en archivo
                    self.save_session_to_file(user)

                    # Guardar config default
                    default_config = {
                        "theme": "dark",
                        "language": "es",
                        "autoPlay": True
                    }
                    self.admin_service.save_user_config(uid, default_config)

                    # Callback de éxito
                    if self.on_auth_success:
                        self.on_auth_success(user)
            else:
                if self.on_auth_error:
                    self.on_auth_error(result.get(
                        "error", "Error desconocido"))
        except Exception as e:
            if self.on_auth_error:
                self.on_auth_error(f"Error en autenticación: {str(e)}")

    def logout(self):
        """Cierra la sesión del usuario actual."""
        self.current_user = None
        self.is_logged_in = False
        self.delete_session_file()

        if self.on_logout_success:
            self.on_logout_success()

    def save_session_to_file(self, user: Dict):
        """Guarda datos de sesión en archivo JSON.
        @param user: Datos del usuario autenticado."""
        try:
            session_data = {
                "localId": user.get("localId"),
                "email": user.get("email"),
                "displayName": user.get("displayName", "Usuario"),
                "idToken": user.get("idToken"),
                "refreshToken": user.get("refreshToken")
            }
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
        except Exception as e:
            print(f"Error guardando sesión: {str(e)}")

    def load_session_from_file(self) -> bool:
        """Carga sesión guardada desde archivo.
        @return: True si se cargó exitosamente, False en caso contrario."""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)

                self.current_user = session_data
                self.is_logged_in = True

                if self.on_session_loaded:
                    self.on_session_loaded(session_data)

                return True
        except Exception as e:
            print(f"Error cargando sesión: {str(e)}")

        return False

    def delete_session_file(self):
        """Elimina el archivo de sesión guardado."""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
        except Exception as e:
            print(f"Error eliminando sesión: {str(e)}")

    def get_current_user_email(self) -> Optional[str]:
        """Obtiene el email del usuario actual.
        @return: Email o None si no hay usuario autenticado."""
        if self.current_user:
            return self.current_user.get("email")
        return None

    def get_current_user_name(self) -> Optional[str]:
        """Obtiene el nombre del usuario actual.
        @return: Nombre o None si no hay usuario autenticado."""
        if self.current_user:
            return self.current_user.get("displayName", "Usuario")
        return None
        self.on_auth_error(result["error"])

    def get_current_user(self):
        return self.admin_service.get_current_user()

    def sign_out(self):
        self.admin_service.sign_out()
