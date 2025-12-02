import pyaudio
import numpy as np
import librosa


class AudioProcessor:
    def __init__(self, device_index=None, chunk=32768, rate=44100, min_energy=0.00004):
        self.p = pyaudio.PyAudio()
        self.RATE = rate
        self.CHUNK = chunk  # Tamaño de bloque de audio. Valores altos mejoran la detección de graves, pero aumentan la latencia. Recomendado: 4096-32768
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.MIN_ENERGY = min_energy  # Sensibilidad mínima para detectar sonido
        self.stream = None
        self.device_index = device_index
        # Para cambiar el micrófono, modifica self.device_index. Usa el script list_microphones.py para ver los índices disponibles.
        if self.device_index is None:
            for i in range(self.p.get_device_count()):
                info = self.p.get_device_info_by_index(i)
                max_input = int(info["maxInputChannels"])
                if max_input > 0:
                    self.device_index = i
                    break

    def start(self):
        try:
            self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS,
                                      rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK,
                                      input_device_index=self.device_index)
            # print(f"[Audio] Micrófono ID {self.device_index} abierto.")
        except Exception as e:
            print(f"[ERROR] No se pudo abrir el micrófono: {e}")
            raise

    def process(self):
        if not self.stream:
            return None, 0.0
        try:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            audio = np.frombuffer(data, dtype=np.int16).astype(
                np.float32) / 32768.0
            energy = np.mean(audio**2)

            if energy > self.MIN_ENERGY:
                # YIN optimizado para bajas frecuencias
                f0 = librosa.yin(audio,
                                 fmin=30,          # Detecta desde 30 Hz
                                 fmax=1318,
                                 sr=self.RATE,
                                 frame_length=self.CHUNK,
                                 hop_length=512)
                freq = np.median(f0[np.isfinite(f0)])
                if 30 <= freq <= 1318:
                    return freq, energy
        except (OSError, ValueError) as e:
            # print(f"[AudioProcessor] Error en process: {e}")
            pass
        return None, energy

    def stop(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
    # print("[Audio] Stream cerrado.")
