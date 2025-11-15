# Para que funcione hay que escribir en la terminal:
# pip install pyaudio numpy librosa tkinter
"""
Afinador de Guitarra Profesional - POO
Funcionalidad completa + ultra estable + frecuencia en vivo
"""

import pyaudio
import numpy as np
import librosa
import math
import time
import tkinter as tk
from tkinter import Canvas
from collections import deque
import threading

# ================================
# CLASE 1: AudioProcessor
# ================================


class AudioProcessor:
    def __init__(self, device_index=1, min_energy=0.0001):
        self.device_index = device_index
        self.MIN_ENERGY = min_energy
        self.CHUNK = 4096
        self.RATE = 44100
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

        self.STABILITY_SEC = 0.35
        self.ENERGY_SMOOTH = 0.9
        self.MAX_FREQ_VARIATION = 0.015  # 1.5%

        self.buffer_size = max(
            1, int(self.RATE / self.CHUNK * self.STABILITY_SEC))
        self.pitch_buffer = deque(maxlen=self.buffer_size)
        self.freq_buffer = deque(maxlen=self.buffer_size)

        self.smoothed_energy = 0.0
        self.last_stable_freq = 0.0

        self.stream = None
        self.p = pyaudio.PyAudio()

    def start(self):
        try:
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                input_device_index=self.device_index
            )
            print(f"[Audio] Micrófono ID {self.device_index} abierto.")
        except Exception as e:
            print(f"[ERROR] No se pudo abrir el micrófono: {e}")
            raise

    def read_frame(self):
        if not self.stream:
            return None, 0.0
        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        audio_int16 = np.frombuffer(data, dtype=np.int16)
        audio_float = audio_int16.astype(np.float32) / 32768.0
        return audio_float, np.mean(audio_float ** 2)

    def process(self):
        audio, energy = self.read_frame()
        if audio is None:
            return None, 0.0, 0.0

        # Suavizar energía
        self.smoothed_energy = (
            self.ENERGY_SMOOTH * self.smoothed_energy +
            (1 - self.ENERGY_SMOOTH) * energy
        )

        if self.smoothed_energy < self.MIN_ENERGY:
            self.pitch_buffer.clear()
            self.freq_buffer.clear()
            return None, self.smoothed_energy, 0.0

        # Ventana de Hann
        window = np.hanning(len(audio))
        audio = audio * window

        # YIN
        f0 = librosa.yin(
            y=audio,
            fmin=librosa.note_to_hz('E2'),
            fmax=librosa.note_to_hz('E6'),
            sr=self.RATE,
            frame_length=self.CHUNK,
            hop_length=self.CHUNK
        )
        valid = f0[np.isfinite(f0)]
        if len(valid) == 0:
            return None, self.smoothed_energy, 0.0

        pitch = np.median(valid)
        self.pitch_buffer.append(pitch)
        self.freq_buffer.append(pitch)

        if len(self.freq_buffer) < self.buffer_size:
            return None, self.smoothed_energy, len(self.freq_buffer) / self.buffer_size

        avg_freq = np.mean(self.freq_buffer)
        std_freq = np.std(self.freq_buffer)

        # Filtro de estabilidad
        if (std_freq / avg_freq < self.MAX_FREQ_VARIATION or
                abs(avg_freq - self.last_stable_freq) / (self.last_stable_freq or 1) < 0.05):
            self.last_stable_freq = avg_freq
            return avg_freq, self.smoothed_energy, 1.0
        else:
            return None, self.smoothed_energy, 0.8  # Inestable

    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        print("[Audio] Stream cerrado.")


# ================================
# CLASE 2: PitchAnalyzer
# ================================
class PitchAnalyzer:
    def __init__(self):
        self.NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E',
                           'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.A4 = 440.0
        self.A4_MIDI = 69

    def freq_to_note(self, freq):
        if freq < 80 or freq > 1318:
            return None, 0
        midi = 12 * math.log2(freq / self.A4) + self.A4_MIDI
        midi_r = round(midi)
        if midi_r < 28 or midi_r > 88:
            return None, 0
        note = self.NOTE_NAMES[midi_r % 12]
        octave = midi_r // 12 - 1
        expected = self.A4 * (2 ** ((midi_r - self.A4_MIDI) / 12))
        cents = 1200 * math.log2(freq / expected) if expected > 0 else 0
        return f"{note}{octave}", round(cents)


# ================================
# CLASE 3: TunerGUI
# ================================
class TunerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Afinador de Guitarra - MUGUI")
        self.root.geometry("580x480")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(False, False)

        # Frecuencia
        self.freq_label = tk.Label(
            self.root, text="--- Hz", font=("Consolas", 26, "bold"),
            fg="#00ffff", bg="#1a1a1a"
        )
        self.freq_label.pack(pady=15)

        # Nota
        self.note_label = tk.Label(
            self.root, text="---", font=("Arial", 72, "bold"),
            fg="#00ff00", bg="#1a1a1a"
        )
        self.note_label.pack(pady=10)

        # Cents
        self.cents_label = tk.Label(
            self.root, text="+0 cents", font=("Arial", 22),
            fg="#ffffff", bg="#1a1a1a"
        )
        self.cents_label.pack(pady=5)

        # Aguja
        self.canvas = Canvas(self.root, width=460, height=130,
                             bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=20)

        center_x = 230
        self.canvas.create_line(center_x, 20, center_x,
                                110, fill="#666666", width=3)
        self.canvas.create_text(center_x, 120, text="0",
                                fill="#ffffff", font=("Arial", 10))
        for i in range(1, 6):
            x = center_x - i * 35
            self.canvas.create_line(x, 50, x, 75, fill="#666666")
            self.canvas.create_text(
                x, 90, text=f"-{i*10}", fill="#ffffff", font=("Arial", 9))
            x = center_x + i * 35
            self.canvas.create_line(x, 50, x, 75, fill="#666666")
            self.canvas.create_text(
                x, 90, text=f"+{i*10}", fill="#ffffff", font=("Arial", 9))

        self.needle = self.canvas.create_line(
            center_x, 65, center_x, 65, fill="#00ff00", width=5)

        # Estado
        self.status_label = tk.Label(
            self.root, text="Esperando señal...", font=("Arial", 11),
            fg="#888888", bg="#1a1a1a"
        )
        self.status_label.pack(pady=5)

        self.stability = 0.0

    def update(self, freq, note, cents, energy, stability):
        self.stability = stability

        # Frecuencia
        if freq and stability >= 1.0:
            self.freq_label.config(text=f"{freq:.2f} Hz", fg="#00ffff")
        else:
            self.freq_label.config(text="--- Hz", fg="#888888")

        # Nota y cents
        if note and stability >= 1.0:
            self.note_label.config(text=note, fg="#00ff00")
            sign = "+" if cents >= 0 else ""
            color = "#00ff00" if abs(cents) <= 10 else "#ffff00"
            self.cents_label.config(text=f"{sign}{cents} cents", fg=color)
            self.status_label.config(text="Afinando...", fg="#00ff00")
            self.move_needle(cents)
        else:
            self.note_label.config(text="---", fg="#888888")
            self.cents_label.config(
                text="Estabilizando..." if stability > 0 else "Sin señal", fg="#aaaa00")
            if stability < 1.0 and stability > 0:
                self.status_label.config(
                    text=f"Estabilizando: {int(stability*100)}%", fg="#aaaa00")
            else:
                self.status_label.config(text="Toca una cuerda", fg="#888888")
            self.move_needle(0)

        self.root.update_idletasks()

    def move_needle(self, cents):
        cents = max(-50, min(50, cents))
        x_offset = (cents / 50) * 180
        x_end = 230 + x_offset
        self.canvas.coords(self.needle, 230, 65, x_end, 65)

    def run(self):
        self.root.mainloop()


# ================================
# CLASE 4: TunerApp (Orquestador)
# ================================
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


# ================================
# MAIN
# ================================
if __name__ == "__main__":
    print("="*60)
    print("    AFINADOR DE GUITARRA PROFESIONAL - MUGUI")
    print("    POO • Ultra Estable • Frecuencia en Vivo")
    print("="*60)
    app = TunerApp()
    app.run()
