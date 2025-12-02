import time
import threading
from mvvm.Model.AudioProcessor import AudioProcessor
from mvvm.Model.PitchAnalyzer import PitchAnalyzer


class TunerApp:
    def __init__(self):
        self.audio = AudioProcessor()  # device_index: Cambia el micrófono aquí
        self.analyzer = PitchAnalyzer()
        self.gui = None  # Se asigna en run

    def run(self, gui):
        self.gui = gui
        self.audio.start()
        audio_thread = threading.Thread(target=self.audio_loop, daemon=True)
        audio_thread.start()
        if self.gui:
            self.gui.run()

    def audio_loop(self):
        while True:
            try:
                result = self.audio.process()
                freq = result[0] if result else None
                energy = result[1] if result else 0
                note, cents, positions, _ = self.analyzer.freq_to_note(freq)
                if self.gui:
                    # Preferir on_audio_update para evitar conflicto con tkinter.Misc.update
                    try:
                        if hasattr(self.gui, 'on_audio_update'):
                            self.gui.on_audio_update(
                                freq, note, cents, positions, energy)
                        elif hasattr(self.gui, 'update'):
                            # llamar solo si la firma es compatible
                            try:
                                self.gui.update(
                                    freq, note, cents, positions, energy)
                            except TypeError:
                                pass
                    except Exception:
                        pass
                time.sleep(0.02)
            except (OSError, ValueError) as e:
                # print(f"[ERROR] {e}")
                break
        self.audio.stop()
