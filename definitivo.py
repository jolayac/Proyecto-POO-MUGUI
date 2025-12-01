
import threading
import time
from mvvm.View.TunerGUI import TunerGUI
from mvvm.ViewModel.TunerApp import TunerApp

# Frame principal: crea el calibrador y el diapasón


def main():
    gui = TunerGUI()
    app = TunerApp()

    def audio_loop():
        while True:
            try:
                result = app.audio.process()
                freq = result[0] if result else None
                energy = result[1] if result else 0
                note, cents, positions, _ = app.analyzer.freq_to_note(freq)
                gui.root.after(0, gui.update, freq, note,
                               cents, positions, energy)
                time.sleep(0.02)
            except (OSError, ValueError) as e:
                print(f"[ERROR] {e}")
                break
        app.audio.stop()

    app.audio.start()
    threading.Thread(target=audio_loop, daemon=True).start()
    gui.run()


if __name__ == "__main__":
    main()
