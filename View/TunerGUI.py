import tkinter as tk
from tkinter import Canvas

class TunerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Afinador de Guitarra - MUGUI")
        self.root.geometry("580x480")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)

        # Frecuencia
        self.freq_label = tk.Label(
            self.root, text="--- Hz", font=("Consolas", 26, "bold"),
            fg="#00ffff", bg="#1a1a1a"
        )
        self.freq_label.pack(pady=15)

        # Nota
        self.note_label = tk.Label(
            self.root, text="---", font=("Arial", 72, "bold"),
            fg="#00ff00", bg="#1a1a1a"
        )
        self.note_label.pack(pady=10)

        # Cents
        self.cents_label = tk.Label(
            self.root, text="+0 cents", font=("Arial", 22),
            fg="#ffffff", bg="#1a1a1a"
        )
        self.cents_label.pack(pady=5)

        # Aguja
        self.canvas = Canvas(self.root, width=460, height=130, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=20)

        center_x = 230
        self.canvas.create_line(center_x, 20, center_x, 110, fill="#666666", width=3)
        self.canvas.create_text(center_x, 120, text="0", fill="#ffffff", font=("Arial", 10))
        for i in range(1, 6):
            x = center_x - i * 35
            self.canvas.create_line(x, 50, x, 75, fill="#666666")
            self.canvas.create_text(x, 90, text=f"-{i*10}", fill="#ffffff", font=("Arial", 9))
            x = center_x + i * 35
            self.canvas.create_line(x, 50, x, 75, fill="#666666")
            self.canvas.create_text(x, 90, text=f"+{i*10}", fill="#ffffff", font=("Arial", 9))

        self.needle = self.canvas.create_line(center_x, 65, center_x, 65, fill="#00ff00", width=5)

        # Estado
        self.status_label = tk.Label(
            self.root, text="Esperando señal...", font=("Arial", 11),
            fg="#888888", bg="#1a1a1a"
        )
        self.status_label.pack(pady=5)

        self.stability = 0.0

    def update(self, freq, note, cents, energy, stability):
        self.stability = stability

        # Frecuencia
        if freq and stability >= 1.0:
            self.freq_label.config(text=f"{freq:.2f} Hz", fg="#00ffff")
        else:
            self.freq_label.config(text="--- Hz", fg="#888888")

        # Nota y cents
        if note and stability >= 1.0:
            self.note_label.config(text=note, fg="#00ff00")
            sign = "+" if cents >= 0 else ""
            color = "#00ff00" if abs(cents) <= 10 else "#ffff00"
            self.cents_label.config(text=f"{sign}{cents} cents", fg=color)
            self.status_label.config(text="Afinando...", fg="#00ff00")
            self.move_needle(cents)
        else:
            self.note_label.config(text="---", fg="#888888")
            self.cents_label.config(text="Estabilizando..." if stability > 0 else "Sin señal", fg="#aaaa00")
            if stability < 1.0 and stability > 0:
                self.status_label.config(text=f"Estabilizando: {int(stability*100)}%", fg="#aaaa00")
            else:
                self.status_label.config(text="Toca una cuerda", fg="#888888")
            self.move_needle(0)

        self.root.update_idletasks()

    def move_needle(self, cents):
        cents = max(-50, min(50, cents))
        x_offset = (cents / 50) * 180
        x_end = 230 + x_offset
        self.canvas.coords(self.needle, 230, 65, x_end, 65)

    def run(self):
        self.root.mainloop()