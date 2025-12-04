# splash_screen.py
import tkinter as tk
from typing import Callable


class SplashScreen:
    """Clase reutilizable para mostrar un splash screen. Recibe un callback para continuar."""

    def __init__(self, parent: tk.Tk, on_complete: Callable[[], None] = None):
        self.parent = parent
        self.on_complete = on_complete

        # Ventana splash
        self.splash = tk.Toplevel(parent)
        self.splash.title("MUGUI")
        self.splash.geometry("500x350")
        self.splash.configure(bg="#1a1a1a")
        self.splash.overrideredirect(True)
        self.splash.resizable(True, True)

        # Centrar
        self.center_window(self.splash, 500, 350)

        # Logo
        try:
            self.logo_img = tk.PhotoImage(file="assets/logo.png")
            tk.Label(self.splash, image=self.logo_img,
                     bg="#1a1a1a").pack(pady=(40, 20))
        except tk.TclError:
            tk.Label(
                self.splash,
                text="MUGUI",
                font=("Helvetica", 36, "bold"),
                fg="#00bfff",
                bg="#1a1a1a"
            ).pack(pady=(60, 10))

        # Texto
        tk.Label(self.splash, text="MUGUI", font=(
            "Helvetica", 28, "bold"), fg="#ecf0f1", bg="#1a1a1a").pack()
        tk.Label(self.splash, text="Cargando...", font=(
            "Helvetica", 14), fg="#bdc3c7", bg="#1a1a1a").pack(pady=(5, 20))

        # Barra de progreso
        self.progress = tk.Canvas(
            self.splash, height=4, bg="#2c3e50", highlightthickness=0)
        self.progress.pack(fill="x", padx=50, pady=10)
        self.progress_bar = self.progress.create_rectangle(
            0, 0, 0, 4, fill="#00bfff")

        # Animar
        self.animate_progress(0)

    def center_window(self, window, width, height):
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def animate_progress(self, value):
        if value > 400:
            # Esperar 1 segundo más antes de cerrar
            self.splash.after(1000, self.finish)
            return
        self.progress.coords(self.progress_bar, 0, 0, value, 4)
        self.splash.after(15, self.animate_progress, value + 8)

    def close(self):
        try:
            self.splash.destroy()
        except:
            pass

    def finish(self):
        """Llamado cuando el splash screen debe terminar y ejecutar callback"""
        self.close()
        if self.on_complete:
            self.on_complete()

    def show(self):
        self.splash.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MUGUI App")
    root.geometry("800x600")

    def on_splash_complete():
        root.deiconify()  # Mostrar ventana principal
        tk.Label(root, text="Ventana Principal de MUGUI",
                 font=("Helvetica", 24)).pack(pady=200)

    splash = SplashScreen(root, on_complete=on_splash_complete)
    splash.show()
    root.mainloop()
