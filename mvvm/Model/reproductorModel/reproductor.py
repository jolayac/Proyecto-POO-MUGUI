import pygame
from mvvm.Model.reproductorModel.pista import Pista


class Reproductor:
    """
    Modelo responsable de la reproducción de audio (usa pygame.mixer).
    Permite agregar pistas, controlar la reproducción y el volumen.
    """

    def __init__(self):
        pygame.mixer.init()
        self.pistas: list[Pista] = []
        self.indice_actual: int = 0
        self.volumen: float = 1.0

    def agregar_rutas(self, rutas: list[str]):
        """Agrega rutas de archivos de audio como pistas."""
        for ruta in rutas:
            self.pistas.append(Pista(ruta))

    def pista_actual(self) -> Pista | None:
        """Devuelve la pista actualmente seleccionada."""
        if not self.pistas:
            return None
        return self.pistas[self.indice_actual]

    def cargar_actual(self):
        """Carga la pista actual en el mezclador."""
        pista = self.pista_actual()
        if pista:
            pygame.mixer.music.load(pista.ruta)

    def reproducir(self):
        """Reproduce la pista actual si está cargada."""
        if not self.pistas:
            return
        self.cargar_actual()
        try:
            pygame.mixer.music.play()
        except pygame.error:
            pass

    def pausar(self):
        """Pausa la reproducción."""
        pygame.mixer.music.pause()

    def continuar(self):
        """Continúa la reproducción pausada."""
        pygame.mixer.music.unpause()

    def detener(self):
        """Detiene la reproducción."""
        pygame.mixer.music.stop()

    def siguiente(self):
        """Avanza a la siguiente pista."""
        if not self.pistas:
            return
        self.indice_actual = (self.indice_actual + 1) % len(self.pistas)
        self.cargar_actual()
        pygame.mixer.music.play()

    def anterior(self):
        """Retrocede a la pista anterior."""
        if not self.pistas:
            return
        self.indice_actual = (self.indice_actual - 1) % len(self.pistas)
        self.cargar_actual()
        pygame.mixer.music.play()

    def establecer_volumen(self, valor: float):
        """Establece el volumen de reproducción (0.0 a 1.0)."""
        self.volumen = max(0.0, min(1.0, valor))
        pygame.mixer.music.set_volume(self.volumen)
