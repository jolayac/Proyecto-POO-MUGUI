from tkinter import Frame
from mvvm.View.afinador.TunerCalibrator import TunerCalibratorFrame
from mvvm.View.afinador.Fretboard import FretboardFrame


class TunerGUI(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#181818")
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
