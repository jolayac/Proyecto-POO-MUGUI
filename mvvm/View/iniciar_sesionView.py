# view/iniciar_sesionView.py
import tkinter as tk
from tkinter import messagebox
from mvvm.ViewModel.authentication_vm import AuthenticationViewModel
from dotenv import load_dotenv

class IniciarSesionView:
    def __init__(self, master=None):
        load_dotenv()
        self.vm = AuthenticationViewModel()
        self.vm.on_auth_success = self.on_login_success
        self.vm.on_auth_error = self.on_login_error

        self.window = tk.Toplevel(master) if master else tk.Tk()
        self.window.title("MUGUI - Iniciar Sesión")
        self.window.geometry("400x500")
        self.window.configure(bg="#34495e")

        tk.Label(self.window, text="Iniciar Sesión en MUGUI", font=("Helvetica", 18, "bold"),
                 fg="#ecf0f1", bg="#34495e").pack(pady=30)

        tk.Label(self.window, text="Usa tu cuenta de Google",
                 fg="#bdc3c7", bg="#34495e", font=("Helvetica", 12)).pack(pady=10)

        btn_google = tk.Button(
            self.window,
            text="Continuar con Google",
            font=("Helvetica", 12, "bold"),
            bg="#4285f4",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            command=self.open_google_signin
        )
        btn_google.pack(pady=30)

        # tk.Label(self.window, text="Este flujo se completa automáticamente:", fg="#bdc3c7", bg="#34495e").pack(pady=(20,5))

    def open_google_signin(self):
        self.vm.start_google_auth("login")

    def confirm_token(self):
        pass

    def on_login_success(self, user):
        messagebox.showinfo("¡Éxito!", f"Bienvenido de nuevo\n{user['email']}")
        self.window.destroy()

    def on_login_error(self, error_msg):
        if "Ya existe una cuenta" in error_msg or "Cuenta ya existe" in error_msg:
            messagebox.showinfo("Redirección", "Ya tienes cuenta. ¡Estás iniciando sesión!")
        else:
            messagebox.showerror("Error", error_msg)

    def main(self):
        self.window.mainloop()


# === MAIN ===
if __name__ == "__main__":
    app = IniciarSesionView()
    app.main()
