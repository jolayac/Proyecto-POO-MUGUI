# View/login_dialog.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading


class LoginDialog:
    """Diálogo para autenticación con Google Firebase."""

    def __init__(self, parent, auth_vm):
        """
        @param parent: Ventana padre (tk.Tk o tk.Toplevel)
        @param auth_vm: Instancia de AuthenticationViewModel
        """
        self.auth_vm = auth_vm
        self.window = tk.Toplevel(parent)
        self.window.title("Iniciar Sesión - MUGUI")
        self.window.geometry("500x300")
        self.window.resizable(False, False)

        # Centrar ventana
        self.window.transient(parent)
        self.window.grab_set()

        # Crear interfaz
        self.setup_ui()

        # Configurar callbacks
        self.auth_vm.on_auth_success = self.on_login_success
        self.auth_vm.on_auth_error = self.on_login_error

    def setup_ui(self):
        """Crea los elementos de la interfaz."""
        # Título
        title_label = ttk.Label(
            self.window,
            text="Autenticación con Google",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=20)

        # Descripción
        desc_label = ttk.Label(
            self.window,
            text="Haz clic en 'Iniciar Sesión' para autenticarte con tu cuenta de Google.\n"
                 "Se abrirá tu navegador web automáticamente.",
            wraplength=450,
            justify="center"
        )
        desc_label.pack(pady=10)

        # Botón de inicio de sesión
        login_button = ttk.Button(
            self.window,
            text="Iniciar Sesión con Google",
            command=self.start_login
        )
        login_button.pack(pady=15)

        # Área para código
        code_label = ttk.Label(
            self.window,
            text="O si deseas, copia el código de autorización aquí:",
            font=("Arial", 9)
        )
        code_label.pack(pady=10)

        code_frame = ttk.Frame(self.window)
        code_frame.pack(pady=5, padx=20, fill="x")

        ttk.Label(code_frame, text="Código:").pack(side="left", padx=5)

        self.code_entry = ttk.Entry(code_frame, width=40)
        self.code_entry.pack(side="left", padx=5, fill="x", expand=True)

        ttk.Button(
            code_frame,
            text="Enviar",
            command=self.process_code
        ).pack(side="left", padx=5)

        # Área de estado
        self.status_label = ttk.Label(
            self.window,
            text="",
            foreground="blue",
            wraplength=450
        )
        self.status_label.pack(pady=10)

    def start_login(self):
        """Inicia el flujo de login automático."""
        self.status_label.config(
            text="Abriendo navegador... Completa la autenticación en el navegador.",
            foreground="blue"
        )
        self.window.update()

        # Ejecutar en thread para no bloquear UI
        thread = threading.Thread(target=self._login_async, daemon=True)
        thread.start()

    def _login_async(self):
        """Ejecuta el login en un thread separado."""
        try:
            url = self.auth_vm.start_google_signin()

            # Mostrar instrucciones al usuario
            self.window.after(0, self._show_code_instruction)
        except Exception as e:
            self.window.after(
                0,
                lambda: messagebox.showerror(
                    "Error", f"Error en autenticación: {str(e)}")
            )

    def _show_code_instruction(self):
        """Muestra instrucciones para copiar el código."""
        self.status_label.config(
            text="Completa la autenticación en el navegador y copia el código de autorización. "
                 "Luego pégalo en el campo arriba y haz clic en 'Enviar'.",
            foreground="darkgreen"
        )

    def process_code(self):
        """Procesa el código de autorización ingresado."""
        code = self.code_entry.get().strip()

        if not code:
            messagebox.showwarning(
                "Código Requerido", "Por favor ingresa el código de autorización.")
            return

        self.status_label.config(
            text="Procesando autenticación...",
            foreground="blue"
        )
        self.window.update()

        # Procesar código en thread
        self.auth_vm.process_google_code(code)

    def on_login_success(self, user: dict):
        """Llamado cuando la autenticación es exitosa."""
        email = user.get("email", "Usuario")
        name = user.get("displayName", "")

        self.window.after(0, lambda: messagebox.showinfo(
            "Autenticación Exitosa",
            f"¡Bienvenido {name or email}!\n\nTu sesión ha sido guardada."
        ))
        self.window.after(0, self.window.destroy)

    def on_login_error(self, error: str):
        """Llamado cuando hay un error en la autenticación."""
        self.window.after(
            0,
            lambda: messagebox.showerror(
                "Error de Autenticación", f"Error: {error}")
        )
        self.status_label.config(
            text="Error en autenticación. Intenta de nuevo.",
            foreground="red"
        )


class LogoutConfirmDialog:
    """Diálogo de confirmación para cerrar sesión."""

    def __init__(self, parent, username: str, on_confirm):
        """
        @param parent: Ventana padre
        @param username: Nombre del usuario a desconectar
        @param on_confirm: Callback cuando se confirma logout
        """
        self.on_confirm = on_confirm

        result = tk.messagebox.askyesno(
            "Cerrar Sesión",
            f"¿Deseas cerrar la sesión de {username}?",
            parent=parent
        )

        if result:
            on_confirm()
