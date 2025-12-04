from tkinter import Frame
from mvvm.View.afinador.TunerCalibrator import TunerCalibratorFrame
from mvvm.View.afinador.Fretboard import FretboardFrame


class TunerGUI(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#181818")

        # Variables para escalado responsivo
        self._base_width = 1400
        self._base_height = 600
        self._scale_factor = 1.0

        # Vincularse a eventos de redimensionamiento
        self.bind("<Configure>", self._on_resize)

        self.calibrator = TunerCalibratorFrame(self)
        self.calibrator.pack(side="left", fill="y", padx=30, pady=30)
        self.fretboard = FretboardFrame(self)
        self.fretboard.pack(side="right", fill="both",
                            expand=True, padx=30, pady=30)

    def on_audio_update(self, freq, note, cents, positions, energy=None):
        """Nuevo nombre para actualizar UI desde el loop de audio.
        Mantengo compatibilidad con otros componentes al definir un alias 'update_alias'."""
        # delegar a los subcomponentes
        try:
            self.calibrator.update(freq, note, cents)
        except Exception:
            pass
        try:
            self.fretboard.update_notes(positions)
        except Exception:
            pass

    # Alias para compatibilidad (no recomendado usar desde fuera)
    update_alias = on_audio_update

    def _on_resize(self, event=None):
        """Maneja el redimensionamiento del frame."""
        try:
            if event and hasattr(event, 'width') and event.width > 1:
                self._scale_factor = event.width / self._base_width
                self._update_fonts()
        except Exception:
            pass

    def _update_fonts(self):
        """Actualiza los tamaños de fuente en los subcomponentes."""
        try:
            # Actualizar calibrador
            if hasattr(self.calibrator, '_update_fonts'):
                self.calibrator._update_fonts(self._scale_factor)

            # Actualizar fretboard
            if hasattr(self.fretboard, '_update_fonts'):
                self.fretboard._update_fonts(self._scale_factor)
        except Exception:
            pass
