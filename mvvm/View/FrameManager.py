"""
FrameManager.py - View para gestión de presentación de frames

Responsabilidades:
- Mostrar/ocultar frames en la aplicación
- Gestionar transiciones entre pantallas
- Delegar lógica de navegación al ViewModel
"""

import threading
import tkinter as tk

from mvvm.ViewModel.FrameNavigationViewModel import FrameNavigationViewModel
from mvvm.View.TunerGUI import TunerGUI
from mvvm.ViewModel.TunerApp import TunerApp
from mvvm.View.metronomo import MetronomeFrame
from mvvm.View.reproductorFrame import ReproductorFrame
from mvvm.View.menu import MenuFrame
from mvvm.View.chords import ChordDetectorView
from mvvm.ViewModel.chords_vm import ChordDetectorViewModel


class FrameManager:
    """View que gestiona la presentación de frames en la aplicación."""

    def __init__(self, root: tk.Tk, main_container: tk.Frame):
        self.root = root
        self.main_container = main_container
        self.nav_vm = FrameNavigationViewModel()

    def cleanup_current_frame(self):
        """Delega limpieza al ViewModel."""
        self.nav_vm.cleanup_current_frame()

    def show_menu(self):
        """Muestra el menú principal."""
        self.cleanup_current_frame()
        self.nav_vm.audio_running = False
        self.root.geometry("1400x600")

        self.nav_vm.current_frame = MenuFrame(
            self.main_container,
            on_tuner_clicked=self.show_tuner,
            on_metronome_clicked=self.show_metronome,
            on_reproductor_clicked=self.show_reproductor,
            on_chords_clicked=self.show_chords
        )
        self.nav_vm.current_frame.pack(fill="both", expand=True)

    def show_tuner(self):
        """Muestra el afinador."""
        self.cleanup_current_frame()
        self.nav_vm.audio_running = True
        self.root.geometry("1400x600")

        self.nav_vm.current_frame = TunerGUI(self.main_container)
        self.nav_vm.current_frame.pack(fill="both", expand=True)

        self.nav_vm.tuner_app = TunerApp()
        self.nav_vm.audio_thread = threading.Thread(
            target=self._audio_loop, daemon=True)
        self.nav_vm.audio_thread.start()

    def show_metronome(self):
        """Muestra el metrónomo."""
        self.cleanup_current_frame()
        self.nav_vm.audio_running = False
        self.root.geometry("1400x600")

        self.nav_vm.current_frame = MetronomeFrame(self.main_container)
        self.nav_vm.current_frame.pack(fill="both", expand=True)

    def show_reproductor(self):
        """Muestra el reproductor."""
        self.cleanup_current_frame()
        self.nav_vm.audio_running = False
        self.root.geometry("1400x600")

        self.nav_vm.current_frame = ReproductorFrame(self.main_container)
        self.nav_vm.current_frame.pack(fill="both", expand=True)

    def show_chords(self):
        """Muestra el detector de acordes."""
        self.cleanup_current_frame()
        self.nav_vm.audio_running = False
        self.root.geometry("1400x600")

        chord_vm = ChordDetectorViewModel()
        self.nav_vm.current_frame = ChordDetectorView(
            chord_vm, self.main_container)
        self.nav_vm.current_frame.pack(fill="both", expand=True)

    def _audio_loop(self):
        """Ejecuta el loop de audio delegando al ViewModel."""
        def on_audio_result(freq, note, cents, positions, energy):
            if self.nav_vm.current_frame and isinstance(self.nav_vm.current_frame, TunerGUI):
                try:
                    if hasattr(self.nav_vm.current_frame, 'on_audio_update'):
                        frame = self.nav_vm.current_frame
                        self.root.after(0, lambda f=frame, fr=freq, n=note, c=cents, p=positions, e=energy:
                                        f.on_audio_update(fr, n, c, p, e) if isinstance(f, TunerGUI) else None)
                except (tk.TclError, RuntimeError):
                    self.nav_vm.audio_running = False

        self.nav_vm.process_audio(on_audio_result)
