"""
MenuViewModel.py - ViewModel para gestión de menús

Responsabilidades:
- Lógica de obtención de datos del menú
- Verificación de estado de autenticación
- Preparación de datos para renderizar en la UI
"""

from typing import Any

from mvvm.ViewModel.authentication_vm import AuthenticationViewModel


class MenuViewModel:
    """ViewModel que gestiona la lógica de la barra de menús."""

    def __init__(self, auth_vm: AuthenticationViewModel):
        self.auth_vm = auth_vm

    def get_account_menu_items(self) -> dict[str, Any]:
        """Retorna los items del menú de cuenta según estado de autenticación."""
        if self.auth_vm.is_logged_in:
            username = self.auth_vm.get_current_user_name() or "Usuario"
            email = self.auth_vm.get_current_user_email() or ""
            return {
                "logged_in": True,
                "username": username,
                "email": email
            }
        else:
            return {"logged_in": False}
