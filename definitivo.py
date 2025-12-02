"""
definitivo.py - MUGUI Application Entry Point

Estructura OOP:
- App: Clase principal que orquesta todo
- FrameManager: Gestión de frames (cambios de pantalla)
- MenuManager: Gestión de menús
- AuthenticationManager: Gestión de autenticación
"""

import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from mvvm.View.TunerGUI import TunerGUI
from mvvm.ViewModel.TunerApp import TunerApp
from mvvm.View.metronomo import MetronomeFrame
from mvvm.View.reproductorFrame import ReproductorFrame
from mvvm.View.splash_screen import SplashScreen
from mvvm.View.login_dialog import LoginDialog, LogoutConfirmDialog
from mvvm.View.menu import MenuFrame
from mvvm.ViewModel.authentication_vm import AuthenticationViewModel


class FrameManager:
    """Gestiona el cambio y limpieza de frames en la aplicación."""

    def __init__(self, root, main_container):
        self.root = root
        self.main_container = main_container
        self.current_frame = None
        self.audio_thread = None
        self.app = None
        self.running = False

    def cleanup_current_frame(self):
        """Limpia el frame actual y detiene procesos asociados."""
        # Detener metrónomo si está activo
        try:
            if isinstance(self.current_frame, MetronomeFrame):
                if hasattr(self.current_frame, 'vm'):
                    try:
                        self.current_frame.vm.stop()
                    except:
                        pass
        except:
            pass

        # Detener reproductor si está activo
        try:
            if isinstance(self.current_frame, ReproductorFrame):
                if hasattr(self.current_frame, 'vm'):
                    try:
                        self.current_frame.vm.detener_actualizador()
                        self.current_frame.vm.detener()
                    except:
                        pass
        except:
            pass

        # Detener afinador (audio thread)
        try:
            if self.audio_thread and self.audio_thread.is_alive():
                self.running = False
                self.audio_thread.join(timeout=1)
            if self.app and hasattr(self.app, 'audio'):
                try:
                    self.app.audio.stop()
                except:
                    pass
        except:
            pass

        # Destruir el frame
        try:
            if self.current_frame:
                self.current_frame.pack_forget()
                self.current_frame.destroy()
                self.current_frame = None
        except:
            pass

    def show_menu(self):
        """Muestra el menú principal."""
        self.cleanup_current_frame()
        self.running = False
        self.root.geometry("1400x600")

        self.current_frame = MenuFrame(
            self.main_container,
            on_tuner_clicked=self.show_tuner,
            on_metronome_clicked=self.show_metronome,
            on_reproductor_clicked=self.show_reproductor
        )
        self.current_frame.pack(fill="both", expand=True)

    def show_tuner(self):
        """Muestra el afinador."""
        self.cleanup_current_frame()
        self.running = True
        self.root.geometry("1400x600")

        self.current_frame = TunerGUI(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

        self.app = TunerApp()
        self.audio_thread = threading.Thread(
            target=self._audio_loop, daemon=True)
        self.audio_thread.start()

    def show_metronome(self):
        """Muestra el metrónomo."""
        self.cleanup_current_frame()
        self.running = False
        self.root.geometry("820x520")

        self.current_frame = MetronomeFrame(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

    def show_reproductor(self):
        """Muestra el reproductor."""
        self.cleanup_current_frame()
        self.running = False
        self.root.geometry("420x200")

        self.current_frame = ReproductorFrame(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

    def _audio_loop(self):
        """Loop de procesamiento de audio (corre en thread separado)."""
        try:
            if not self.app or not hasattr(self.app, 'audio'):
                return

            self.app.audio.start()
            while self.running and self.current_frame:
                try:
                    result = self.app.audio.process()
                    freq = result[0] if result else None
                    energy = result[1] if result else 0

                    if self.app and hasattr(self.app, 'analyzer'):
                        note, cents, positions, _ = self.app.analyzer.freq_to_note(
                            freq)

                        if self.current_frame and isinstance(self.current_frame, TunerGUI):
                            try:
                                if hasattr(self.current_frame, 'on_audio_update'):
                                    frame = self.current_frame
                                    self.root.after(0, lambda f=frame, fr=freq, n=note, c=cents, p=positions, e=energy:
                                                    f.on_audio_update(fr, n, c, p, e) if isinstance(f, TunerGUI) else None)
                            except (tk.TclError, RuntimeError):
                                break

                    time.sleep(0.02)
                except (OSError, ValueError, AttributeError):
                    break
        finally:
            try:
                if self.app and hasattr(self.app, 'audio'):
                    self.app.audio.stop()
            except:
                pass


class MenuManager:
    """Gestiona los menús de la aplicación."""

    def __init__(self, root, frame_manager, auth_manager):
        self.root = root
        self.frame_manager = frame_manager
        self.auth_manager = auth_manager
        self.menu_bar = None
        self.account_menu = None

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
        self.menu_bar.add_cascade(label="Funciones", menu=functions_menu)

        # Menú Cuenta
        self.account_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.update_account_menu()
        self.menu_bar.add_cascade(label="Cuenta", menu=self.account_menu)

        self.root.config(menu=self.menu_bar)

    def update_account_menu(self):
        """Actualiza el menú de Cuenta según estado de autenticación."""
        self.account_menu.delete(0, tk.END)

        if self.auth_manager.is_logged_in():
            username = self.auth_manager.get_current_user_name()
            email = self.auth_manager.get_current_user_email()

            self.account_menu.add_command(
                label=f"Usuario: {username} ({email})",
                state="disabled"
            )
            self.account_menu.add_separator()
            self.account_menu.add_command(
                label="Cerrar Sesión",
                command=self.auth_manager.logout_with_confirmation
            )
        else:
            self.account_menu.add_command(
                label="Iniciar Sesión",
                command=self.auth_manager.show_login_dialog
            )
            self.account_menu.add_command(
                label="Registrarse",
                command=self.auth_manager.show_login_dialog
            )


class AuthenticationManager:
    """Gestiona la autenticación y sesiones."""

    def __init__(self, root, menu_manager):
        self.root = root
        self.menu_manager = menu_manager
        self.auth_vm = AuthenticationViewModel()

        # Configurar callbacks
        self.auth_vm.on_session_loaded = self._on_session_loaded
        self.auth_vm.on_auth_success = self._on_auth_success

    def initialize(self):
        """Inicializa el ViewModel de autenticación."""
        # Cargar sesión guardada si existe
        if hasattr(self.auth_vm, 'load_session_from_file'):
            self.auth_vm.load_session_from_file()

    def is_logged_in(self):
        """Retorna si el usuario está autenticado."""
        return self.auth_vm.is_logged_in

    def get_current_user_name(self):
        """Retorna el nombre del usuario actual."""
        return self.auth_vm.get_current_user_name() or "Usuario"

    def get_current_user_email(self):
        """Retorna el email del usuario actual."""
        return self.auth_vm.get_current_user_email() or ""

    def show_login_dialog(self):
        """Abre el diálogo de inicio de sesión."""
        LoginDialog(self.root, self.auth_vm)

    def logout_with_confirmation(self):
        """Cierra la sesión con confirmación del usuario."""
        username = self.get_current_user_name()

        def confirm_logout():
            self.auth_vm.logout()
            messagebox.showinfo(
                "Sesión Cerrada",
                "Tu sesión ha sido cerrada exitosamente."
            )
            self.menu_manager.update_account_menu()

        LogoutConfirmDialog(self.root, username, confirm_logout)

    def _on_session_loaded(self, user_data: dict):
        """Callback cuando se carga una sesión guardada."""
        # Actualizar menú inmediatamente
        self.menu_manager.update_account_menu()

    def _on_auth_success(self, user_data: dict):
        """Callback cuando la autenticación es exitosa."""
        # Actualizar menú inmediatamente - AQUI ESTÁ LA CLAVE
        self.menu_manager.update_account_menu()


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

        # Crear managers en orden de dependencias
        self.frame_manager = FrameManager(self.root, self.main_container)
        self.menu_manager = MenuManager(self.root, self.frame_manager, None)
        self.auth_manager = AuthenticationManager(self.root, self.menu_manager)

        # Actualizar referencia en menu_manager
        self.menu_manager.auth_manager = self.auth_manager

        # Crear menú
        self.menu_manager.create_menu()

        # Inicializar autenticación (carga sesiones guardadas)
        self.auth_manager.initialize()

        # Mostrar splash screen
        self.splash = SplashScreen(
            self.root,
            on_complete=self._show_main_frame
        )
        self.splash.show()

    def _show_main_frame(self):
        """Mostrado cuando splash screen termina."""
        self.root.deiconify()
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
