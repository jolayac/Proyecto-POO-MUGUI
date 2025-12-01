import tkinter as tk
from tkinter import Canvas, messagebox
import threading
import time
import pyaudio
import numpy as np
import librosa
import math
from collections import deque

class AudioProcessor:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.RATE = 44100
        self.CHUNK = 32768                 # ← MÁXIMO POSIBLE (clave para graves)
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

        self.MIN_ENERGY = 0.00004          # ← ULTRA sensible para 6ª y 5ª cuerda
        self.stream = None
        self.device_index = None
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                self.device_index = i
                break

    def start(self):
        try:
            self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS,
                                     rate=self.RATE, input=True,
                                     frames_per_buffer=self.CHUNK,
                                     input_device_index=self.device_index)
        except Exception as e:
            messagebox.showerror("Error", f"Micrófono no disponible:\n{e}")
            raise

    def process(self):
        if not self.stream: return None, 0.0
        try:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            energy = np.mean(audio**2)

            if energy > self.MIN_ENERGY:
                # YIN OPTIMIZADO AL MÁXIMO PARA BAJAS FRECUENCIAS
                f0 = librosa.yin(audio, 
                                 fmin=30,          # ← Detecta desde 30 Hz
                                 fmax=1318, 
                                 sr=self.RATE,
                                 frame_length=32768,   # ← más largo = mejor graves
                                 hop_length=512)       # ← más resolución
                freq = np.median(f0[np.isfinite(f0)])
                if 30 <= freq <= 1318:
                    return freq, energy
        except: pass
        return None, energy

    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

# =================== LÓGICA PERFECTA DE CUERDA/TRASTE ===================
class PitchAnalyzer:
    # Afinación estándar (frecuencias exactas de cuerdas al aire)
    OPEN_STRINGS = [82.41, 110.00, 146.83, 196.00, 246.94, 329.63]  # E2 A2 D3 G3 B3 E4
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    A4 = 440.0

    def freq_to_note(self, freq):
        if freq < 40:
            return f"{freq:.1f}Hz", 0, 0, 0

        # Nota y cents
        midi = 69 + 12 * math.log2(freq / self.A4)
        note_num = round(midi) % 12
        octave = int(round(midi)) // 12 - 1
        note_name = self.NOTES[note_num] + str(octave)
        cents = int(1200 * math.log2(freq / (self.A4 * 2**((round(midi)-69)/12))))

        # ------------------ PRIORIDAD: CUERDA AL AIRE ------------------
        for string, open_freq in enumerate(self.OPEN_STRINGS, 1):
            cents_diff = abs(1200 * math.log2(freq / open_freq))
            if cents_diff <= 25:
                return note_name, cents, 7-string, 0

        best_string = 6
        best_fret = 0
        min_diff = float('inf')

        for string, base in enumerate(self.OPEN_STRINGS, 1):
            for fret in range(1, 25):
                note_freq = base * (2 ** (fret / 12.0))
                diff = abs(note_freq - freq)
                if diff < min_diff:
                    min_diff = diff
                    best_string = 7 - string
                    best_fret = fret

        return note_name, cents, best_string, best_fret

# =================== GUI (sin cambios importantes) ===================
class TunerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Afinador + Tablatura - MUGUI")
        self.root.geometry("1200x620")
        self.root.configure(bg="#0f0f0f")
        self.root.resizable(False, False)

        main = tk.Frame(self.root, bg="#0f0f0f")
        main.pack(fill="both", expand=True)

        # Izquierda
        left = tk.Frame(main, bg="#0f0f0f")
        left.pack(side="left", padx=50, pady=40)

        self.freq_label = tk.Label(left, text="--- Hz", font=("Consolas", 36), fg="#00ffff", bg="#0f0f0f")
        self.freq_label.pack(pady=10)
        self.note_label = tk.Label(left, text="---", font=("Arial", 110, "bold"), fg="#00ff44", bg="#0f0f0f")
        self.note_label.pack(pady=10)
        self.cents_label = tk.Label(left, text="±0 cents", font=("Arial", 38), fg="#ffffff", bg="#0f0f0f")
        self.cents_label.pack(pady=10)

        self.canvas_aguja = Canvas(left, width=600, height=140, bg="#0f0f0f", highlightthickness=0)
        self.canvas_aguja.pack(pady=20)
        self._dibujar_aguja()

        self.status = tk.Label(left, text="Toca una cuerda", font=("Arial", 18), fg="#88ff88", bg="#0f0f0f")
        self.status.pack(pady=10)

        # Derecha - Tablatura
        right = tk.Frame(main, bg="#0f0f0f")
        right.pack(side="right", padx=70, pady=60)

        tk.Label(right, text="TABLATURA", font=("Arial", 24, "bold"), fg="#00ff88", bg="#0f0f0f").pack(pady=10)
        self.canvas_tab = Canvas(right, width=420, height=360, bg="#1a1a1a", highlightthickness=2, highlightbackground="#333")
        self.canvas_tab.pack()
        self.dibujar_tablatura_base()
        self.tab_text = self.canvas_tab.create_text(210, 335, text="Toca una nota...", font=("Arial", 16), fill="#888888")

    def _dibujar_aguja(self):
        cx = 300
        self.canvas_aguja.create_line(cx, 20, cx, 120, fill="#555", width=6)
        for i in range(-5, 6):
            x = cx + i*50
            self.canvas_aguja.create_line(x, 70, x, 100, fill="#777", width=5)
            self.canvas_aguja.create_text(x, 115, text=f"{i*10}", fill="#ccc", font=("Arial", 12))
        self.needle = self.canvas_aguja.create_line(cx, 80, cx, 80, fill="#00ff44", width=10)

    def dibujar_tablatura_base(self):
        for i in range(6):
            y = 80 + i*45
            self.canvas_tab.create_line(60, y, 360, y, fill="#aaa", width=2)
        for i, n in enumerate("654321"):
            self.canvas_tab.create_text(40, 80 + i*45, text=n, fill="#888", font=("Arial", 14, "bold"))

    def dibujar_tablatura(self, string, fret):
        self.canvas_tab.delete("fret")
        if string == 0:
            self.canvas_tab.itemconfig(self.tab_text, text="Toca una nota...")
            return
        y = 80 + (6-string)*45
        txt = str(fret) if fret > 0 else "0"
        self.canvas_tab.create_text(210, y, text=txt, font=("Arial", 40, "bold"), fill="#00ff88", tags="fret")
        self.canvas_tab.itemconfig(self.tab_text, text=f"Cuerda {string} – Traste {fret}")

    def update(self, freq, note, cents, string, fret, energy):
        if freq:
            self.freq_label.config(text=f"{freq:.2f} Hz", fg="#00ffff")
            self.note_label.config(text=note, fg="#00ff44")
            color = "#00ff44" if abs(cents) <= 10 else "#ffff00" if abs(cents) <= 25 else "#ff4444"
            self.cents_label.config(text=f"{cents:+d} cents", fg=color)
            self.status.config(text="¡Perfecto!" if abs(cents) <= 10 else "Afinando...", fg=color)
            self.canvas_aguja.coords(self.needle, 300, 80, 300 + (cents/50)*260, 80)
            self.dibujar_tablatura(string, fret)
        else:
            self.status.config(text="Toca una cuerda", fg="#888888")
            self.canvas_aguja.coords(self.needle, 300, 80, 300, 80)
            self.dibujar_tablatura(0, 0)

class TunerApp:
    def __init__(self):
        self.audio = AudioProcessor()
        self.analyzer = PitchAnalyzer()
        self.gui = TunerGUI()

    def run(self):
        try:
            self.audio.start()
            threading.Thread(target=self._loop, daemon=True).start()
            self.gui.root.mainloop()
        finally:
            self.audio.stop()

    def _loop(self):
        while True:
            result = self.audio.process()
            freq = result[0] if result else None
            note, cents, string, fret = self.analyzer.freq_to_note(freq) if freq else (None, 0, 0, 0)
            self.gui.root.after(0, self.gui.update, freq, note, cents, string, fret, result[1] if result else 0)
            time.sleep(0.02)

def lanzar_afinador():
    TunerApp().run()

if __name__ == "__main__":
    lanzar_afinador()