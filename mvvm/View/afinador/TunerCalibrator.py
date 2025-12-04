import tkinter as tk
from tkinter import Canvas, Frame


class TunerCalibratorFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#1a1a1a")

        # Variables para escalado responsivo
        self._base_width = 350
        self._scale_factor = 1.0
        self.bind("<Configure>", self._on_resize)

        self.freq_label = tk.Label(
            self, text="--- Hz", font=("Consolas", 26, "bold"), fg="#00ffff", bg="#1a1a1a")
        self.freq_label.pack(pady=15)
        self.note_label = tk.Label(
            self, text="---", font=("Arial", 72, "bold"), fg="#00ff00", bg="#1a1a1a")
        self.note_label.pack(pady=10)
        self.cents_label = tk.Label(
            self, text="+0 cents", font=("Arial", 22), fg="#ffffff", bg="#1a1a1a")
        self.cents_label.pack(pady=5)
        self.canvas = Canvas(self, width=460, height=130,
                             bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=20)
        center_x = 230
        self.canvas.create_line(center_x, 20, center_x,
                                110, fill="#666666", width=3)
        self.canvas.create_text(center_x, 120, text="0",
                                fill="#ffffff", font=("Arial", 10))
        for i in range(1, 6):
            x = center_x - i * 35
            self.canvas.create_line(x, 50, x, 75, fill="#666666")
            self.canvas.create_text(
                x, 90, text=f"-{i*10}", fill="#ffffff", font=("Arial", 9))
            x = center_x + i * 35
            self.canvas.create_line(x, 50, x, 75, fill="#666666")
            self.canvas.create_text(
                x, 90, text=f"+{i*10}", fill="#ffffff", font=("Arial", 9))
        self.needle = self.canvas.create_line(
            center_x, 65, center_x, 65, fill="#00ff00", width=5)
        self.status_label = tk.Label(self, text="Esperando...", font=(
            "Arial", 11), fg="#888888", bg="#1a1a1a")
        self.status_label.pack(pady=5)
        self.last_freq = None
        self.last_note = None
        self.last_cents = None

    def update(self, freq, note, cents):
        # Mantener la última nota y cents si no hay nueva
        if freq:
            self.last_freq = freq
        if note:
            self.last_note = note
        if note is not None:
            self.last_cents = cents
        # Frecuencia
        if self.last_freq is not None:
            self.freq_label.config(
                text=f"{self.last_freq:.2f} Hz", fg="#00ffff")
        else:
            self.freq_label.config(text="--- Hz", fg="#888888")
        # Nota y cents
        if self.last_note is not None and self.last_cents is not None:
            sign = "+" if self.last_cents >= 0 else ""
            color = "#00ff00" if abs(self.last_cents) <= 10 else "#ffff00"
            self.note_label.config(text=self.last_note, fg="#00ff00")
            self.cents_label.config(
                text=f"{sign}{self.last_cents} cents", fg=color)
            # Se puede escribir un mensaje mientras está afinando.
            self.status_label.config(text="", fg="#00ff00")
            self.move_needle(self.last_cents)
        else:
            self.note_label.config(text="---", fg="#888888")
            self.cents_label.config(text="Escuchando...", fg="#aaaa00")
            self.status_label.config(text="Toca una cuerda", fg="#888888")
            self.move_needle(0)
        self.update_idletasks()

    def move_needle(self, cents):
        cents = max(-50, min(50, cents))
        x_offset = (cents / 50) * 180
        x_end = 230 + x_offset
        self.canvas.coords(self.needle, 230, 65, x_end, 65)

    def _on_resize(self, event=None):
        """Maneja el redimensionamiento del frame."""
        try:
            if event and hasattr(event, 'width') and event.width > 1:
                self._scale_factor = event.width / self._base_width
                self._update_fonts()
        except Exception:
            pass

    def _update_fonts(self, scale_factor=None):
        """Actualiza los tamaños de fuente según el factor de escala."""
        try:
            if scale_factor is not None:
                self._scale_factor = scale_factor

            freq_size = max(18, int(26 * self._scale_factor))
            note_size = max(48, int(72 * self._scale_factor))
            cents_size = max(16, int(22 * self._scale_factor))
            status_size = max(8, int(11 * self._scale_factor))

            self.freq_label.config(font=("Consolas", freq_size, "bold"))
            self.note_label.config(font=("Arial", note_size, "bold"))
            self.cents_label.config(font=("Arial", cents_size))
            self.status_label.config(font=("Arial", status_size))
        except Exception:
            pass
