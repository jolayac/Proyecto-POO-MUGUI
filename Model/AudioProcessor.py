import pyaudio
import numpy as np
import librosa
from collections import deque

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

        self.buffer_size = max(1, int(self.RATE / self.CHUNK * self.STABILITY_SEC))
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