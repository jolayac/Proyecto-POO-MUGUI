from typing import List

import tkinter as tk

from mvvm.ViewModel.chords_vm import ChordDetectorViewModel, ChordDetectionResult


class ChordDetectorView(tk.Frame):
    def __init__(self, view_model: ChordDetectorViewModel, parent=None) -> None:
        super().__init__(parent)
        self._view_model = view_model

        self.title_label = tk.Label(
            self, text="Detector de acordes", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)

        self.chord_label = tk.Label(
            self, text="Pulsa 'Analizar' y toca un acorde", font=("Helvetica", 16))
        self.chord_label.pack(pady=10)

        self.detail_label = tk.Label(
            self, text="", font=("Helvetica", 10), justify=tk.LEFT)
        self.detail_label.pack(pady=5)

        self.analyze_button = tk.Button(
            self,
            text="Analizar",
            font=("Helvetica", 14),
            command=self.on_analyze_click,
        )
        self.analyze_button.pack(pady=10)

        self.info_label = tk.Label(
            self,
            text="La aplicación grabará unos segundos desde el micrófono y luego estimará el acorde.",
            font=("Helvetica", 10),
        )
        self.info_label.pack(pady=10)

        self.canvas = tk.Canvas(self, width=500, height=200, bg="white")
        self.canvas.pack(pady=10)

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

        width = int(self.canvas["width"])
        height = int(self.canvas["height"])

        margin = 30
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

        self.canvas.create_line(x0, y0_axis, x1, y0_axis, fill="black")
        self.canvas.create_line(x0, y0_axis, x0, y1_axis, fill="black")

        self.canvas.create_text(
            (x0 + x1) / 2,
            height - 5,
            text="Frecuencia / Nota",
            font=("Helvetica", 9),
            anchor="s",
        )
        self.canvas.create_text(
            5,
            (y0_axis + y1_axis) / 2,
            text="Intensidad",
            font=("Helvetica", 9),
            anchor="w",
        )

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
                x - 5, y0_bar, x + 5, y1, fill="skyblue")

            label = labels[i] if i < len(labels) else ""
            text = f"{label}\n{f:.0f} Hz"
            text_y = max(y0_bar - 2, y1_axis + 2)
            self.canvas.create_text(
                x, text_y, text=text, font=("Helvetica", 8), anchor="s")

    def run(self) -> None:
        self.mainloop()
