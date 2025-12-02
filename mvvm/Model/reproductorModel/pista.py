import mutagen


class Pista:
    """
    Clase que representa una pista de audio.
    Permite obtener información relevante como nombre y duración.
    """

    def __init__(self, ruta: str):
        self.ruta = ruta
        self._info = None

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del archivo de la pista."""
        return self.ruta.replace('\\', '/').split('/')[-1]

    def cargar_info(self):
        """Carga la información de la pista usando mutagen."""
        if self._info is None:
            try:
                self._info = mutagen.File(self.ruta)
            except Exception:
                self._info = None
        return self._info

    def duracion_segundos(self) -> int:
        """Devuelve la duración de la pista en segundos."""
        info = self.cargar_info()
        if info is None or not hasattr(info, 'info'):
            return 0
        return int(info.info.length)

