import threading
import time
import tkinter as tk
from tkinter import ttk
from mvvm.View.TunerGUI import TunerGUI
from mvvm.ViewModel.TunerApp import TunerApp
from mvvm.View.metronomo import MetronomeFrame
from mvvm.View.splash_screen import SplashScreen


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MUGUI App")
        self.root.geometry("800x600")
        self.current_frame = None

        # Crear menú
        self.create_menu()

        # Mostrar splash screen
        self.splash = SplashScreen(self.root, on_complete=self.show_main_frame)
        self.splash.show()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        functions_menu = tk.Menu(menu_bar, tearoff=0)
        functions_menu.add_command(label="Afinador", command=self.show_tuner)
        functions_menu.add_command(label="Metrónomo", command=self.show_metronome)
        menu_bar.add_cascade(label="Funciones", menu=functions_menu)
        self.root.config(menu=menu_bar)

    def show_main_frame(self):
        self.splash.close()
        self.show_tuner()  # Mostrar el afinador por defecto

    def show_tuner(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = TunerGUI()
        app = TunerApp()
        threading.Thread(target=self.audio_loop, daemon=True, args=(app,)).start()

    def show_metronome(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MetronomeFrame(self.root)

    def audio_loop(self, app):
        app.audio.start()
        while True:
            try:
                result = app.audio.process()
                freq = result[0] if result else None
                energy = result[1] if result else 0
                note, cents, positions, _ = app.analyzer.freq_to_note(freq)
                self.root.after(0, self.current_frame.update, freq, note, cents, positions, energy)
                time.sleep(0.02)
            except (OSError, ValueError) as e:
                print(f"[ERROR] {e}")
                break
        app.audio.stop()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()