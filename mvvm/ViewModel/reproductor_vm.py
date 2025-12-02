from tkinter import filedialog
import threading
import time
from mvvm.Model.reproductorModel.reproductor import Reproductor


class ReproductorViewModel:
    """
    ViewModel que conecta la vista con el modelo Reproductor.
    Proporciona métodos para controlar la reproducción y actualizar la interfaz de usuario.
    """

    def __init__(self):
        self.modelo = Reproductor()
        self._actualizaciones = []
        self._ejecutando = False
        self._update_thread = None

    def track_length(self) -> int:
        """Devuelve la duración de la pista actual (alias para barra de tiempo)."""
        return self.duracion_pista()

    def agregar_callback_actualizacion(self, cb):
        """Agrega un callback que se llamará periódicamente para actualizar la UI."""
        self._actualizaciones.append(cb)

    def notificar(self):
        for cb in self._actualizaciones:
            try:
                cb()
            except Exception:
                pass

    def abrir_archivos(self):
        rutas = filedialog.askopenfilenames(
            initialdir='/', title='Escoger la canción(es)', filetype=(('Archivos mp3', '*.mp3*'), ('Todos los archivos', '*.*')))
        if rutas:
            self.modelo.agregar_rutas(list(rutas))
            self.modelo.indice_actual = 0
            return True
        return False

    def reproducir(self):
        self.modelo.reproducir()
        self.iniciar_actualizador()

    def pausar(self):
        self.modelo.pausar()
        self.detener_actualizador()

    def detener(self):
        self.modelo.detener()
        self.detener_actualizador()

    def siguiente(self):
        self.modelo.siguiente()
        # Reiniciar actualizador si estaba ejecutándose
        if self._ejecutando:
            self.detener_actualizador()
            self.iniciar_actualizador()

    def anterior(self):
        self.modelo.anterior()
        # Reiniciar actualizador si estaba ejecutándose
        if self._ejecutando:
            self.detener_actualizador()
            self.iniciar_actualizador()

    def establecer_volumen(self, v):
        """Recibe el valor de la UI (0..10) y lo ajusta a 0..1 para el modelo."""
        self.modelo.establecer_volumen(float(v) * 0.1)

    def pista_actual(self):
        return self.modelo.pista_actual()

    def duracion_pista(self) -> int:
        pista = self.pista_actual()
        if not pista:
            return 0
        return pista.duracion_segundos()

    def posicion_reproduccion_segundos(self) -> int:
        """Devuelve la posición actual de reproducción en segundos."""
        try:
            ms = self._pygame_get_pos()
            if ms < 0:  # -1 significa que no hay reproducción
                return 0
            return int(ms * 0.001)
        except Exception:
            return 0

    def _pygame_get_pos(self):
        try:
            import pygame
            pos = pygame.mixer.music.get_pos()
            return pos
        except Exception:
            return -1

    def iniciar_actualizador(self):
        if self._ejecutando:
            return
        self._ejecutando = True

        def run():
            while self._ejecutando:
                try:
                    self.notificar()
                except Exception:
                    pass
                # Aumentar frecuencia de actualización (50ms en lugar de 100ms)
                time.sleep(0.05)

        self._update_thread = threading.Thread(target=run, daemon=True)
        self._update_thread.start()

    def detener_actualizador(self):
        self._ejecutando = False
        # Esperar a que el thread termine
        if self._update_thread and self._update_thread.is_alive():
            try:
                self._update_thread.join(timeout=0.5)
            except Exception:
                pass

    def continuar(self):
        self.modelo.continuar()
        self.iniciar_actualizador()
        self.iniciar_actualizador()
