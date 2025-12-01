# view/registrarView.py
import tkinter as tk
from tkinter import messagebox
from ViewModel.authentication_vm import AuthenticationViewModel
from dotenv import load_dotenv




class RegistrarView:
    def __init__(self, master=None):
        load_dotenv()
        self.vm = AuthenticationViewModel()
        self.vm.on_auth_success = self.on_register_success
        self.vm.on_auth_error = self.on_register_error

        self.window = tk.Toplevel(master) if master else tk.Tk()
        self.window.title("MUGUI - Registrarse")
        self.window.geometry("400x500")
        self.window.configure(bg="#2c3e50")

        # Título
        tk.Label(self.window, text="¡Bienvenido a MUGUI!", font=(
            "Helvetica", 18, "bold"), fg="#ecf0f1", bg="#2c3e50").pack(pady=30)

        tk.Label(self.window, text="Regístrate con tu cuenta de Google",
                 fg="#bdc3c7", bg="#2c3e50", font=("Helvetica", 12)).pack(pady=10)

        # Botón Google (abre página de Google Sign-In)
        btn_google = tk.Button(
            self.window,
            text="Registrarse con Google",
            font=("Helvetica", 12, "bold"),
            bg="#db4437",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.open_google_signin
        )
        btn_google.pack(pady=30)

        # tk.Label(self.window, text="Este flujo se completa automáticamente.", fg="#bdc3c7", bg="#2c3e50").pack(pady=(20, 5))

    def open_google_signin(self):
        self.vm.start_google_auth("register")

    def on_register_success(self, user):
        messagebox.showinfo(
            "Éxito", f"¡Cuenta creada!\nBienvenido {user['email']}")
        self.window.destroy()  # Cerrar ventana

    def on_register_error(self, error_msg):
        messagebox.showerror("Error al registrarse", error_msg)

    def main(self):
        self.window.mainloop()


# === MAIN ===
if __name__ == "__main__":
    app = RegistrarView()
    app.main()
