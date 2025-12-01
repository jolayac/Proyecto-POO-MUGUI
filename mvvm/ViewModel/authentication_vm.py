# viewmodel/authentication_vm.py
from Model.firebase_admin import FirebaseAdmin
from typing import Callable

class AuthenticationViewModel:
    """ViewModel que conecta las vistas con FirebaseAdmin (auth + RTDB)."""

    def __init__(self):
        self.admin_service = FirebaseAdmin()
        self.on_auth_success: Callable[[dict], None] = None
        self.on_auth_error: Callable[[str], None] = None
        self.on_config_loaded: Callable[[dict], None] = None  # Callback opcional para config cargada

    def start_google_signin(self) -> str:
        """Inicia el flujo de Google Sign-In devolviendo la URL de auth.
        @return: URL para abrir en navegador."""
        return self.admin_service.get_google_auth_url()

    def process_google_code(self, code: str):
        """Procesa el código de Google: intercambia por id_token, autentica y maneja config.
        @param code: Código copiado de Google."""
        exchange = self.admin_service.exchange_code_for_id_token(code)
        if not exchange["success"]:
            if self.on_auth_error:
                self.on_auth_error(exchange["error"])
            return

        id_token = exchange["id_token"]
        result = self.admin_service.sign_in_with_google(id_token)
        if result["success"]:
            user = result["user"]
            uid = user.get("localId")  # UID de Firebase
            if uid:
                # Guardar config default si es nuevo (o siempre, según lógica)
                default_config = {
                    "theme": "dark",
                    "language": "es",
                    "autoPlay": True
                }
                self.admin_service.save_user_config(uid, default_config)
                
                # Cargar config (por si ya existía o se actualizó)
                config = self.admin_service.load_user_config(uid)
                if self.on_config_loaded:
                    self.on_config_loaded(config)
                
                if self.on_auth_success:
                    self.on_auth_success(user)
        else:
            if self.on_auth_error:
                self.on_auth_error(result["error"])

    def get_current_user(self):
        return self.admin_service.get_current_user()

    def sign_out(self):
        self.admin_service.sign_out()