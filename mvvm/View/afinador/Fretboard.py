from tkinter import Canvas, Frame


class FretboardFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#222222")

        # Variables para escalado responsivo
        self._base_width = 600
        self._base_height = 320
        self._scale_factor = 1.0
        self.bind("<Configure>", self._on_resize)

        self.canvas = Canvas(self, width=600, height=320,
                             bg="#222222", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10, fill="both", expand=True)
        self.draw_fretboard()
        self.note_boxes = []
        self.last_positions = []

    def draw_fretboard(self):
        self.canvas.delete("all")

        # Calcular tamaños escalados basados en el ancho del canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1:
            canvas_width = 600
        if canvas_height <= 1:
            canvas_height = 320

        # Escala
        scale_x = canvas_width / 600
        scale_y = canvas_height / 320

        # Posiciones escaladas
        x_start = int(40 * scale_x)
        x_end = int(560 * scale_x)
        y_start = int(40 * scale_y)
        y_end = int(240 * scale_y)
        fret_spacing = int(27 * scale_x)
        string_spacing = int(40 * scale_y)

        # Dibujar cuerdas
        for i in range(6):
            y = y_start + i * string_spacing
            self.canvas.create_line(x_start, y, x_end, y, fill="#aaa", width=2)

        # Dibujar trastes
        for fret in range(20):
            x = x_start + fret * fret_spacing
            self.canvas.create_line(x, y_start, x, y_end, fill="#888", width=1)
            if fret > 0:
                text_size = max(8, int(9 * self._scale_factor))
                self.canvas.create_text(x, int(250 * scale_y), text=str(fret),
                                        fill="#ccc", font=("Arial", text_size))

    def update_notes(self, positions):
        # Mantener las últimas posiciones si no hay nuevas
        if positions:
            self.last_positions = positions
        self.draw_fretboard()

        # Calcular escala para las posiciones
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1:
            canvas_width = 600
        if canvas_height <= 1:
            canvas_height = 320

        scale_x = canvas_width / 600
        scale_y = canvas_height / 320

        x_start = int(40 * scale_x)
        y_start = int(40 * scale_y)
        fret_spacing = int(27 * scale_x)
        string_spacing = int(40 * scale_y)

        # Marcar posiciones de la nota
        for string, fret in self.last_positions:
            x = x_start + fret * fret_spacing
            y = y_start + (string - 1) * string_spacing

            box_size = max(8, int(10 * self._scale_factor))
            self.canvas.create_rectangle(
                x - box_size, y - box_size, x + box_size, y + box_size,
                fill="#00ff88", outline="#005544", width=2)

            dot_size = max(10, int(12 * self._scale_factor))
            self.canvas.create_text(
                x, y, text="●", fill="#222", font=("Arial", dot_size, "bold"))

    def _on_resize(self, event=None):
        """Maneja el redimensionamiento del frame."""
        try:
            if event and hasattr(event, 'width') and event.width > 1:
                self._scale_factor = event.width / self._base_width
                self._update_fonts()
        except Exception:
            pass

    def _update_fonts(self, scale_factor=None):
        """Redibuja el fretboard con tamaños escalados."""
        try:
            if scale_factor is not None:
                self._scale_factor = scale_factor

            # Redibujar el fretboard con el nuevo tamaño
            self.draw_fretboard()
        except Exception:
            pass
