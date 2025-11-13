import sounddevice as sd
import numpy as np
from scipy.fft import rfft, rfftfreq
import math

CHUNK = 2048
RATE = 44100

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
A4 = 440.0

def freq_to_note(freq):
    if freq < 65: return "Silencio", 0
    h = round(12 * math.log2(freq / A4)) + 69
    return f"{NOTE_NAMES[h % 12]}{h//12 - 1}", round(1200 * math.log2(freq / (A4 * 2**((h-69)/12))))

def callback(indata, frames, time, status):
    audio = indata[:, 0]
    window = np.hanning(len(audio))
    audio = audio * window
    fft = rfft(audio)
    mag = np.abs(fft)
    freqs = rfftfreq(len(audio), 1/RATE)
    peak = np.argmax(mag[1:]) + 1
    f = freqs[peak]
    if mag[peak] < 1e6:
        print("Silencio        ", end='\r')
    else:
        note, cents = freq_to_note(f)
        print(f"{f:6.1f} Hz → {note} ({cents:+3} cents)     ", end='\r')

print(sd.query_devices())
with sd.InputStream(samplerate=RATE, channels=1, blocksize=CHUNK, device=1, callback=callback):
    print("Escuchando... (Ctrl+C para salir)")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nDetenido.")