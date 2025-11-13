# mugui_main_window.py
import tkinter as tk
from View.registrarView import RegistrarView
from View.iniciar_sesionView import IniciarSesionView
from View.splash_screen import SplashScreen


class MuguiMainWindow:
    """Ventana principal con botones de login y registro"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.withdraw()

    def show(self):
        self.root.deiconify()
        self.root.title("MUGUI")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="MUGUI", font=("Helvetica", 18, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(pady=20)

        tk.Button(
            self.root, text="Registrarse", font=("Helvetica", 12, "bold"),
            bg="#db4437", fg="white", relief="flat", padx=20, pady=10,
            command=self.open_register
        ).pack(pady=10)

        tk.Button(
            self.root, text="Iniciar Sesión", font=("Helvetica", 12, "bold"),
            bg="#4285f4", fg="white", relief="flat", padx=20, pady=10,
            command=self.open_login
        ).pack(pady=10)

    def open_register(self):
        RegistrarView(self.root)

    def open_login(self):
        IniciarSesionView(self.root)


# === INICIO DE LA APP (main al final) ===
def main():
    root = tk.Tk()
    root.withdraw()

    # Crear ventana principal
    main_window = MuguiMainWindow(root)

    # Mostrar splash y luego la ventana principal
    splash = SplashScreen(root, duration=2500, on_complete=main_window.show)
    splash.show()

    root.mainloop()


if __name__ == "__main__":
    main()