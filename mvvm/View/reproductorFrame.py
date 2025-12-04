from tkinter import Frame
from mvvm.ViewModel.reproductor_vm import ReproductorViewModel
from mvvm.View.reproductorView.reproductorUI import VistaReproductor


class ReproductorFrame(Frame):
    """
    Frame embebible que contiene el reproductor de música.
    Se integra dentro de la ventana principal de MainApp.
    """

    def __init__(self, master=None):
        super().__init__(master, bg="#1a1a1a")

        # Variables para escalado responsivo
        self._base_width = 420
        self._base_height = 200
        self._scale_factor = 1.0
        self.bind("<Configure>", self._on_resize)

        # Crear el ViewModel del reproductor
        self.vm = ReproductorViewModel()

        # Crear la vista del reproductor dentro de este Frame
        self.vista = VistaReproductor(self, self.vm)

    def _on_resize(self, event=None):
        """Maneja el redimensionamiento del frame."""
        try:
            if event and hasattr(event, 'width') and event.width > 1:
                self._scale_factor = event.width / self._base_width
                self._update_fonts()
        except Exception:
            pass

    def _update_fonts(self, scale_factor=None):
        """Actualiza los tamaños de fuente en la vista del reproductor."""
        try:
            if scale_factor is not None:
                self._scale_factor = scale_factor

            if hasattr(self.vista, '_update_fonts'):
                self.vista._update_fonts(self._scale_factor)
        except Exception:
            pass
