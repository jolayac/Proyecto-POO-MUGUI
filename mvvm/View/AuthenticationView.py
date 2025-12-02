"""
AuthenticationView.py - View para gestión de autenticación

Responsabilidades:
- Mostrar diálogos de inicio de sesión y registro
- Mostrar diálogos de confirmación de cierre de sesión
- Actualizar UI cuando cambia estado de autenticación
"""

from tkinter import messagebox
import tkinter as tk

from mvvm.ViewModel.authentication_vm import AuthenticationViewModel
from mvvm.View.login_dialog import LoginDialog, LogoutConfirmDialog


class AuthenticationView:
    """View que gestiona la presentación de diálogos de autenticación."""

    def __init__(self, root: tk.Tk, auth_vm: AuthenticationViewModel, menu_manager: 'MenuManager'):
        self.root = root
        self.auth_vm = auth_vm
        self.menu_manager = menu_manager

        # Configurar callbacks
        self.auth_vm.on_session_loaded = self._on_session_loaded
        self.auth_vm.on_auth_success = self._on_auth_success

    def initialize(self):
        """Inicializa el ViewModel de autenticación."""
        # Cargar sesión guardada si existe
        if hasattr(self.auth_vm, 'load_session_from_file'):
            self.auth_vm.load_session_from_file()

    def show_login_dialog(self):
        """Abre el diálogo de inicio de sesión."""
        LoginDialog(self.root, self.auth_vm)

    def logout_with_confirmation(self):
        """Cierra la sesión con confirmación del usuario."""
        username = self.auth_vm.get_current_user_name() or "Usuario"

        def confirm_logout():
            self.auth_vm.logout()
            messagebox.showinfo(
                "Sesión Cerrada",
                "Tu sesión ha sido cerrada exitosamente."
            )
            self.menu_manager.update_account_menu()

        LogoutConfirmDialog(self.root, username, confirm_logout)

    def _on_session_loaded(self, _user_data: dict):
        """Callback cuando se carga una sesión guardada."""
        # Actualizar menú inmediatamente
        self.menu_manager.update_account_menu()

    def _on_auth_success(self, _user_data: dict):
        """Callback cuando la autenticación es exitosa."""
        # Actualizar menú inmediatamente
        self.menu_manager.update_account_menu()
