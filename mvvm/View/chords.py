from typing import List

import tkinter as tk

from mvvm.ViewModel.chords_vm import ChordDetectorViewModel, ChordDetectionResult


class ChordDetectorView(tk.Frame):
    def __init__(self, view_model: ChordDetectorViewModel, parent=None) -> None:
        super().__init__(parent, bg="#1a1a1a")
        self._view_model = view_model

        # Variables para escalado responsivo
        self._base_width = 800
        self._base_height = 600
        self._scale_factor = 1.0

        # Vincularse a eventos de redimensionamiento
        self.bind("<Configure>", self._on_resize)

        self.title_label = tk.Label(
            self, text="Detector de acordes", font=("Helvetica", 18, "bold"),
            bg="#1a1a1a", fg="#fee8d0")
        self.title_label.pack(pady=10)

        self.chord_label = tk.Label(
            self, text="Pulsa 'Analizar' y toca un acorde", font=("Helvetica", 16),
            bg="#1a1a1a", fg="#fee8d0")
        self.chord_label.pack(pady=10)

        self.detail_label = tk.Label(
            self, text="", font=("Helvetica", 10), justify=tk.LEFT,
            bg="#1a1a1a", fg="#cccccc")
        self.detail_label.pack(pady=5)

        self.analyze_button = tk.Button(
            self,
            text="Analizar",
            font=("Helvetica", 14),
            command=self.on_analyze_click,
            bg="#FC6E20", fg="black"
        )
        self.analyze_button.pack(pady=10)

        self.info_label = tk.Label(
            self,
            text="La aplicación grabará unos segundos desde el micrófono y luego estimará el acorde.",
            font=("Helvetica", 10),
            bg="#1a1a1a", fg="#cccccc"
        )
        self.info_label.pack(pady=10)

        # Frame para centrar el canvas
        canvas_frame = tk.Frame(self, bg="#1a1a1a")
        canvas_frame.pack(pady=10, fill="both", expand=True, padx=20)

        # Canvas con fondo #323232
        self.canvas = tk.Canvas(
            canvas_frame, width=500, height=200, bg="#323232", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.after(200, self._check_result_queue)

    def on_analyze_click(self) -> None:
        self.chord_label.config(text="Grabando... toca tu acorde ahora")
        self.analyze_button.config(state=tk.DISABLED)
        self._view_model.analyze_once_async()

    def _check_result_queue(self) -> None:
        try:
            while True:
                result = self._view_model.result_queue.get_nowait()

                if isinstance(result, ChordDetectionResult):
                    self.chord_label.config(text=result.summary_text)
                    self.detail_label.config(text=result.detail_text)
                    self._draw_frequency_diagram(
                        result.dominant_freqs,
                        result.note_labels,
                        result.magnitudes,
                    )
                else:
                    self.chord_label.config(text=str(result))

                self.analyze_button.config(state=tk.NORMAL)
        except Exception:
            # Cola vacía u otro problema menor en la lectura; simplemente seguimos
            pass

        self.after(200, self._check_result_queue)

    def _draw_frequency_diagram(
        self,
        freqs: List[float],
        labels: List[str],
        mags: List[float],
    ) -> None:
        self.canvas.delete("all")
        if not freqs:
            return

        width = int(self.canvas.winfo_width())
        height = int(self.canvas.winfo_height())

        if width <= 1:
            width = 500
        if height <= 1:
            height = 200

        margin = 40
        bar_max_height = height - 2 * margin
        n = len(freqs)
        if n <= 0:
            return

        step = (width - 2 * margin) / max(n, 1)

        if mags and max(mags) > 0:
            max_mag = max(mags)
        else:
            max_mag = 1.0

        x0 = margin
        y0_axis = height - margin
        x1 = width - margin
        y1_axis = margin

        # Dibujar ejes
        self.canvas.create_line(x0, y0_axis, x1, y0_axis,
                                fill="#888888", width=2)
        self.canvas.create_line(x0, y0_axis, x0, y1_axis,
                                fill="#888888", width=2)

        # Etiquetas de ejes
        self.canvas.create_text(
            (x0 + x1) / 2,
            height - 5,
            text="Frecuencia / Nota",
            font=("Helvetica", 9),
            anchor="s",
            fill="#cccccc"
        )
        self.canvas.create_text(
            5,
            (y0_axis + y1_axis) / 2,
            text="Intensidad",
            font=("Helvetica", 9),
            anchor="w",
            fill="#cccccc"
        )

        # Dibujar barras con color #fee8d0
        for i, f in enumerate(freqs):
            x = margin + (i + 0.5) * step
            mag = mags[i] if i < len(mags) else max_mag
            norm = mag / max_mag
            if norm < 0:
                norm = 0
            if norm > 1:
                norm = 1
            bar_height = bar_max_height * norm
            y1 = y0_axis
            y0_bar = max(y1 - bar_height, y1_axis + 5)
            self.canvas.create_rectangle(
                x - 5, y0_bar, x + 5, y1, fill="#fee8d0", outline="#ffb380", width=1)

            label = labels[i] if i < len(labels) else ""
            text = f"{label}\n{f:.0f} Hz"
            text_y = max(y0_bar - 2, y1_axis + 2)
            self.canvas.create_text(
                x, text_y, text=text, font=("Helvetica", 8), anchor="s", fill="#cccccc")

    def _on_resize(self, event=None) -> None:
        """Maneja el redimensionamiento del frame."""
        try:
            if event and hasattr(event, 'width') and event.width > 1:
                self._scale_factor = event.width / self._base_width
                self._update_fonts()
        except Exception:
            pass

    def _update_fonts(self) -> None:
        """Actualiza los tamaños de fuente según el factor de escala."""
        try:
            title_size = max(14, int(18 * self._scale_factor))
            chord_size = max(12, int(16 * self._scale_factor))
            detail_size = max(9, int(10 * self._scale_factor))
            button_size = max(12, int(14 * self._scale_factor))
            info_size = max(9, int(10 * self._scale_factor))

            self.title_label.config(font=("Helvetica", title_size, "bold"))
            self.chord_label.config(font=("Helvetica", chord_size))
            self.detail_label.config(font=("Helvetica", detail_size))
            self.analyze_button.config(font=("Helvetica", button_size))
            self.info_label.config(font=("Helvetica", info_size))
        except Exception:
            pass

    def run(self) -> None:
        self.mainloop()
