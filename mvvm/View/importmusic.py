import pygame
from tkinter import filedialog
import time

class MusicImporter:

    @staticmethod
    def import_music():
        try:
            pygame.mixer.init()
        except Exception:
            pass

        ruta_cancion = filedialog.askopenfilename(
            title="Selecciona tu canción",
            filetypes=[("Archivos de audio", "*.mp3 *.wav")]
        )

        if not ruta_cancion:
            print("No se seleccionó ningún archivo.")
            return

        try:
            pygame.mixer.music.load(ruta_cancion)
            pygame.mixer.music.play()
        except Exception as e:
            print("Error al reproducir:", e)
            return

        while pygame.mixer.music.get_busy():
            time.sleep(0.5)


