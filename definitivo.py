import threading
import time
import tkinter as tk
from tkinter import ttk
from mvvm.View.TunerGUI import TunerGUI
from mvvm.ViewModel.TunerApp import TunerApp
from mvvm.View.metronomo import MetronomeFrame
from mvvm.View.reproductorFrame import ReproductorFrame
from mvvm.View.splash_screen import SplashScreen


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MUGUI App")
        self.root.geometry("1400x600")
        self.root.withdraw()  # Ocultar ventana principal al inicio

        self.current_frame = None
        self.audio_thread = None
        self.app = None
        self.running = True
        self.main_container = None  # Se inicializará antes del splash

        # Crear menú
        self.create_menu()

        # Inicializar contenedor ANTES de mostrar splash screen
        self.initialize_main_container()

        # Mostrar splash screen
        self.splash = SplashScreen(self.root, on_complete=self.show_main_frame)
        self.splash.show()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        functions_menu = tk.Menu(menu_bar, tearoff=0)
        functions_menu.add_command(label="Afinador", command=self.show_tuner)
        functions_menu.add_command(
            label="Metrónomo", command=self.show_metronome)
        functions_menu.add_command(
            label="Reproductor", command=self.show_reproductor)
        menu_bar.add_cascade(label="Funciones", menu=functions_menu)
        self.root.config(menu=menu_bar)

    def initialize_main_container(self):
        """Inicializa el contenedor principal (se ejecuta ANTES del splash)"""
        self.main_container = tk.Frame(self.root, bg="#1a1a1a")
        self.main_container.pack(fill="both", expand=True)

    def show_main_frame(self):
        """Llamado cuando splash screen termina"""
        # Mostrar ventana principal
        self.root.deiconify()
        # Mostrar afinador por defecto
        self.show_tuner()

    def cleanup_current_frame(self):
        """Limpia el frame actual y detiene procesos asociados"""
        # Detener metrónomo si está activo
        try:
            if isinstance(self.current_frame, MetronomeFrame):
                if hasattr(self.current_frame, 'vm'):
                    try:
                        self.current_frame.vm.stop()
                    except:
                        pass
        except:
            pass

        # Detener reproductor si está activo
        try:
            if isinstance(self.current_frame, ReproductorFrame):
                if hasattr(self.current_frame, 'vm'):
                    try:
                        self.current_frame.vm.detener_actualizador()
                        self.current_frame.vm.detener()
                    except:
                        pass
        except:
            pass

        # Detener afinador (audio thread)
        try:
            if self.audio_thread and self.audio_thread.is_alive():
                self.running = False
                # Esperar a que el thread termine
                self.audio_thread.join(timeout=1)
            if self.app and hasattr(self.app, 'audio'):
                try:
                    self.app.audio.stop()
                except:
                    pass
        except:
            pass

        # Destruir el frame
        try:
            if self.current_frame:
                self.current_frame.pack_forget()
                self.current_frame.destroy()
                self.current_frame = None
        except:
            pass

    def show_tuner(self):
        """Muestra el afinador como frame embebible"""
        self.cleanup_current_frame()
        self.running = True

        # Ajustar tamaño de ventana para el afinador
        self.root.geometry("1400x600")

        # Crear TunerGUI como Frame dentro del contenedor principal
        self.current_frame = TunerGUI(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

        # Iniciar thread de audio
        self.app = TunerApp()
        self.audio_thread = threading.Thread(
            target=self.audio_loop, daemon=True)
        self.audio_thread.start()

    def show_metronome(self):
        """Muestra el metrónomo como frame embebible"""
        self.cleanup_current_frame()
        self.running = False

        # Ajustar tamaño de ventana para el metrónomo
        self.root.geometry("820x520")

        # Crear MetronomeFrame dentro del contenedor principal
        self.current_frame = MetronomeFrame(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

    def show_reproductor(self):
        """Muestra el reproductor como frame embebible"""
        self.cleanup_current_frame()
        self.running = False

        # Ajustar tamaño de ventana para el reproductor
        self.root.geometry("420x200")

        # Crear ReproductorFrame dentro del contenedor principal
        self.current_frame = ReproductorFrame(self.main_container)
        self.current_frame.pack(fill="both", expand=True)

    def audio_loop(self):
        """Loop de procesamiento de audio (corre en thread separado)"""
        try:
            if not self.app or not hasattr(self.app, 'audio'):
                return

            self.app.audio.start()
            while self.running and self.current_frame:
                try:
                    result = self.app.audio.process()
                    freq = result[0] if result else None
                    energy = result[1] if result else 0

                    if self.app and hasattr(self.app, 'analyzer'):
                        note, cents, positions, _ = self.app.analyzer.freq_to_note(
                            freq)

                        # Actualizar UI de forma segura SOLO si es TunerGUI
                        if self.current_frame and isinstance(self.current_frame, TunerGUI):
                            try:
                                if hasattr(self.current_frame, 'on_audio_update'):
                                    # Capturar valores en la lambda para evitar cambios de referencia
                                    frame = self.current_frame
                                    self.root.after(0, lambda f=frame, fr=freq, n=note, c=cents, p=positions, e=energy:
                                                    f.on_audio_update(fr, n, c, p, e) if isinstance(f, TunerGUI) else None)
                            except (tk.TclError, RuntimeError):
                                break

                    time.sleep(0.02)
                except (OSError, ValueError, AttributeError):
                    break
        finally:
            try:
                if self.app and hasattr(self.app, 'audio'):
                    self.app.audio.stop()
            except:
                pass

    def on_closing(self):
        """Llamado cuando se cierra la ventana"""
        self.running = False
        self.cleanup_current_frame()
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
