"""
FrameNavigationViewModel.py - ViewModel para gestión de navegación entre frames

Responsabilidades:
- Lógica de navegación entre frames
- Gestión de threads de audio
- Limpieza de recursos
"""

import threading
import time
import tkinter as tk
from typing import Optional, Any, Callable

from mvvm.ViewModel.TunerApp import TunerApp


class FrameNavigationViewModel:
    """ViewModel que gestiona la lógica de navegación entre frames."""

    def __init__(self):
        self.current_frame: Optional[tk.Widget] = None
        self.audio_thread: Optional[threading.Thread] = None
        self.tuner_app: Optional[TunerApp] = None
        self.audio_running: bool = False

    def cleanup_current_frame(self):
        """Limpia el frame actual y detiene procesos asociados."""
        # Importar aquí para evitar imports circulares
        from mvvm.View.metronomo import MetronomeFrame
        from mvvm.View.reproductorFrame import ReproductorFrame

        # Detener metrónomo si está activo
        try:
            if isinstance(self.current_frame, MetronomeFrame):
                if hasattr(self.current_frame, 'vm'):
                    try:
                        self.current_frame.vm.stop()
                    except Exception:
                        pass
        except Exception:
            pass

        # Detener reproductor si está activo
        try:
            if isinstance(self.current_frame, ReproductorFrame):
                if hasattr(self.current_frame, 'vm'):
                    try:
                        self.current_frame.vm.detener_actualizador()
                        self.current_frame.vm.detener()
                    except Exception:
                        pass
        except Exception:
            pass

        # Detener afinador (audio thread)
        try:
            if self.audio_thread and self.audio_thread.is_alive():
                self.audio_running = False
                self.audio_thread.join(timeout=1)
            if self.tuner_app and hasattr(self.tuner_app, 'audio'):
                try:
                    self.tuner_app.audio.stop()
                except Exception:
                    pass
        except Exception:
            pass

        # Destruir el frame
        try:
            if self.current_frame:
                self.current_frame.pack_forget()
                self.current_frame.destroy()
                self.current_frame = None
        except Exception:
            pass

    def process_audio(self, callback: Callable):
        """Loop de procesamiento de audio (corre en thread separado)."""
        try:
            if not self.tuner_app or not hasattr(self.tuner_app, 'audio'):
                return

            self.tuner_app.audio.start()
            while self.audio_running and self.current_frame:
                try:
                    result = self.tuner_app.audio.process()
                    freq = result[0] if result else None
                    energy = result[1] if result else 0

                    if self.tuner_app and hasattr(self.tuner_app, 'analyzer'):
                        note, cents, positions, _ = self.tuner_app.analyzer.freq_to_note(
                            freq)
                        callback(freq, note, cents, positions, energy)

                    time.sleep(0.02)
                except (OSError, ValueError, AttributeError):
                    break
        finally:
            try:
                if self.tuner_app and hasattr(self.tuner_app, 'audio'):
                    self.tuner_app.audio.stop()
            except Exception:
                pass
