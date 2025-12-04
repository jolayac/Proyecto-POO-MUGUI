"""
MenuManager.py - View para gestión de menús

Responsabilidades:
- Crear la barra de menú
- Actualizar elementos del menú según estado
- Vincular acciones de menú a callbacks
"""

from typing import Optional
import tkinter as tk

from mvvm.ViewModel.MenuViewModel import MenuViewModel
from mvvm.ViewModel.authentication_vm import AuthenticationViewModel


class MenuManager:
    """View que gestiona la presentación de menús."""

    def __init__(self, root: tk.Tk, frame_manager: 'FrameManager', auth_vm: AuthenticationViewModel):
        self.root = root
        self.frame_manager = frame_manager
        self.menu_vm = MenuViewModel(auth_vm)
        self.auth_view: Optional['AuthenticationView'] = None
        self.menu_bar: Optional[tk.Menu] = None
        self.account_menu: Optional[tk.Menu] = None

    def set_auth_view(self, auth_view: 'AuthenticationView'):
        """Configura la vista de autenticación (para evitar circular imports)."""
        self.auth_view = auth_view

    def create_menu(self):
        """Crea la barra de menú."""
        self.menu_bar = tk.Menu(self.root)

        # Menú Inicio
        inicio_menu = tk.Menu(self.menu_bar, tearoff=0)
        inicio_menu.add_command(
            label="Menú Principal",
            command=self.frame_manager.show_menu
        )
        self.menu_bar.add_cascade(label="Inicio", menu=inicio_menu)

        # Menú Funciones
        functions_menu = tk.Menu(self.menu_bar, tearoff=0)
        functions_menu.add_command(
            label="Afinador",
            command=self.frame_manager.show_tuner
        )
        functions_menu.add_command(
            label="Metrónomo",
            command=self.frame_manager.show_metronome
        )
        functions_menu.add_command(
            label="Reproductor",
            command=self.frame_manager.show_reproductor
        )
        functions_menu.add_command(
            label="Acordes",
            command=self.frame_manager.show_chords
        )
        self.menu_bar.add_cascade(label="Funciones", menu=functions_menu)

        # Menú Cuenta
        self.account_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.update_account_menu()
        self.menu_bar.add_cascade(label="Cuenta", menu=self.account_menu)

        self.root.config(menu=self.menu_bar)

    def update_account_menu(self):
        """Actualiza el menú de Cuenta según estado de autenticación."""
        if not self.account_menu:
            return

        self.account_menu.delete(0, tk.END)

        menu_data = self.menu_vm.get_account_menu_items()

        if menu_data["logged_in"]:
            username = menu_data["username"]
            email = menu_data["email"]

            self.account_menu.add_command(
                label=f"Usuario: {username} ({email})",
                state="disabled"
            )
            self.account_menu.add_separator()
            self.account_menu.add_command(
                label="Cerrar Sesión",
                command=self.auth_view.logout_with_confirmation if self.auth_view else lambda: None
            )
        else:
            self.account_menu.add_command(
                label="Iniciar Sesión",
                command=self.auth_view.show_login_dialog if self.auth_view else lambda: None
            )
            self.account_menu.add_command(
                label="Registrarse",
                command=self.auth_view.show_login_dialog if self.auth_view else lambda: None
            )
