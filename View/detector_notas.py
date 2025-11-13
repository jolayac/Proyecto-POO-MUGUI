import sounddevice as sd
import numpy as np
import aubio
import librosa

    # ---------- CONFIGURACIÓN ----------
SAMPLERATE = 44100
WIN_S = 1024
HOP_S = 512

    # Inicializar detector de frecuencia
class DetectorNotas:
    pitch_detector = aubio.pitch("default", WIN_S, HOP_S, SAMPLERATE)
    pitch_detector.set_unit("Hz")
    pitch_detector.set_silence(-40)  # Ignora ruidos débiles

    print("🎙️ Escuchando el micrófono... (Ctrl + C para detener)\n")

    # ---------- PROCESAMIENTO DE AUDIO ----------
    def audio_callback(indata, frames, time, status):
        if status:
            print(status)

        audio_data = np.copy(indata[:, 0])

        freq = pitch_detector(audio_data)[0]

        if freq > 0:
            # Convertir frecuencia a nota musical
            nota = librosa.hz_to_note(freq)
            print(f"Nota: {nota:<4} | Frecuencia: {freq:7.2f} Hz")

    # ----- CAPTURA EN TIEMPO REAL -----
    try:
        with sd.InputStream(channels=1, callback=audio_callback, samplerate=SAMPLERATE):
            while True:
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\n🎵 Detección detenida por el usuario.")