import tkinter as tk

from mvvm.View.FrameManager import FrameManager
from mvvm.View.MenuManager import MenuManager
from mvvm.View.AuthenticationView import AuthenticationView
from mvvm.View.splash_screen import SplashScreen
from mvvm.ViewModel.authentication_vm import AuthenticationViewModel


class MainApp:
    """Clase principal que orquesta toda la aplicación."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MUGUI App")
        self.root.geometry("1400x600")
        self.root.withdraw()  # Ocultar al inicio

        # Crear contenedor principal
        self.main_container = tk.Frame(self.root, bg="#1a1a1a")
        self.main_container.pack(fill="both", expand=True)

        # Crear ViewModel de autenticación
        self.auth_vm = AuthenticationViewModel()

        # Crear managers en orden de dependencias
        self.frame_manager = FrameManager(self.root, self.main_container)
        self.menu_manager = MenuManager(
            self.root, self.frame_manager, self.auth_vm)
        self.auth_view = AuthenticationView(
            self.root, self.auth_vm, self.menu_manager)

        # Configurar referencia cruzada para evitar imports circulares
        self.menu_manager.set_auth_view(self.auth_view)

        # Crear menú
        self.menu_manager.create_menu()

        # Inicializar autenticación (carga sesiones guardadas)
        self.auth_view.initialize()

        # Mostrar splash screen
        self.splash = SplashScreen(
            self.root,
            on_complete=self._show_main_frame
        )
        self.splash.show()

    def _show_main_frame(self):
        """Mostrado cuando splash screen termina."""
        self.root.deiconify()   #deiconify esirve para mostrar la ventana que estaba oculta
        # Mostrar menú principal por defecto
        self.frame_manager.show_menu()

    def _on_closing(self):
        """Llamado cuando se cierra la ventana."""
        self.frame_manager.cleanup_current_frame()
        self.root.destroy()

    def run(self):
        """Ejecuta la aplicación."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()



