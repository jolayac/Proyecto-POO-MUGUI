import time
import threading
from Model.AudioProcessor import AudioProcessor
from Model.PitchAnalyzer import PitchAnalyzer
from View.TunerGUI import TunerGUI

class TunerApp:
    def __init__(self):
        self.audio = AudioProcessor(device_index=1, min_energy=0.0001)
        self.analyzer = PitchAnalyzer()
        self.gui = TunerGUI()

    def run(self):
        self.audio.start()
        audio_thread = threading.Thread(target=self.audio_loop, daemon=True)
        audio_thread.start()
        self.gui.run()

    def audio_loop(self):
        while True:
            try:
                result = self.audio.process()
                if result is None:
                    time.sleep(0.01)
                    continue

                freq, energy, stability = result
                if freq:
                    note, cents = self.analyzer.freq_to_note(freq)
                else:
                    note, cents = None, 0

                self.gui.update(freq, note, cents, energy, stability)
                time.sleep(0.01)

            except Exception as e:
                print(f"[ERROR] {e}")
                break

        self.audio.stop()