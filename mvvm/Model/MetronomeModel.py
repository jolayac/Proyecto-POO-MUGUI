# Modelo del metrónomo: encapsula la generación de sonido y recursos de audio.
import os
from typing import Optional
import sys

# Intentar usar pygame para sonidos; si no está, usar winsound en Windows o fallback audible bell.
try:
    import pygame
    import numpy as _np  # usado solo si pygame está disponible
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=256)
    pygame.mixer.init()
    _USING_PYGAME = True
except Exception:
    pygame = None
    _np = None
    _USING_PYGAME = False

if not _USING_PYGAME and sys.platform.startswith("win"):
    try:
        import winsound  # type: ignore
    except Exception:
        winsound = None
else:
    winsound = None


class MetronomeModel:
    """
    Modelo responsable de producir el sonido del click.
    - Si pygame está disponible, intenta cargar sonidos tic.wav / tac.wav desde la carpeta 'sonidos'.
    - Si no existen, crea sonidos sintéticos con numpy (si está disponible).
    - Si nada, usa winsound (Windows) o beep de sistema.
    """

    def __init__(self):
        self.using_pygame = _USING_PYGAME and pygame is not None
        self.has_numpy = _np is not None
        self.has_winsound = winsound is not None
        self.click_accent = None
        self.click_normal = None

        # Intentar cargar los WAV proporcionados en la carpeta 'sonidos' en el root del proyecto
        tic_path = None
        tac_path = None
        try:
            # Si estamos en ejecutable de PyInstaller, usar sys._MEIPASS
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                # En desarrollo: subir 3 directorios desde Model
                base_path = os.path.dirname(
                    os.path.dirname(os.path.dirname(__file__)))

            tic_path = os.path.join(base_path, "sonidos", "tic.wav")
            tac_path = os.path.join(base_path, "sonidos", "tac.wav")
        except Exception:
            pass

        if self.using_pygame:
            loaded = False
            try:
                if tic_path and os.path.exists(tic_path) and tac_path and os.path.exists(tac_path):
                    self.click_normal = pygame.mixer.Sound(tic_path)
                    self.click_accent = pygame.mixer.Sound(tac_path)
                    loaded = True
            except Exception:
                loaded = False

            # Si no se pudieron cargar los WAV, intentar generar sonidos sintéticos si numpy está disponible
            if not loaded and self.has_numpy:
                try:
                    self.click_accent = self._make_sound(
                        1000, 0.08, 0.9)  # frecuencia / duración / volumen
                    self.click_normal = self._make_sound(800, 0.06, 0.6)
                    loaded = True
                except Exception:
                    loaded = False

            # Si no se pudo cargar ni generar, dejar en None y usar fallback
        else:
            # no pygame: nothing to preload
            pass

    def _make_sound(self, freq_hz: int, duration_s: float, volume: float):
        """Generar un pygame.Sound a partir de numpy (si está disponible)."""
        if not self.has_numpy or not self.using_pygame:
            return None
        try:
            fs = 44100
            t = _np.linspace(0, duration_s, int(fs * duration_s), False)
            wave = _np.sin(2 * _np.pi * freq_hz * t) * volume
            wave = _np.int16(wave * 32767)
            sound = pygame.sndarray.make_sound(wave)
            return sound
        except Exception:
            return None

    def play_click(self, accent: bool = False):
        """Reproducir el click; silenciosamente ignorar fallos."""
        try:
            # Preferir pygame sounds si disponibles
            if self.using_pygame:
                s = self.click_accent if accent else self.click_normal
                if s:
                    s.play()
                    return
            # Si pygame no está o no hay sonidos, intentar winsound en Windows
            if self.has_winsound:
                freq = 1000 if accent else 800
                dur = 120 if accent else 80
                try:
                    winsound.Beep(freq, dur)  # type: ignore
                    return
                except Exception:
                    pass
            # Fallback simple (puede no sonar en todos los entornos)
            print("\a", end="", flush=True)
        except Exception:
            # Nunca propagar excepción a la UI
            pass
