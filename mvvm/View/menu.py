"""
menu.py - Vista de Menú Principal

Proporciona una pantalla de bienvenida con la imagen de logo
y botones para acceder a los diferentes módulos de la aplicación.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


class MenuFrame(ttk.Frame):
    """
    Frame que actúa como menú principal de bienvenida.

    Incluye:
    - Imagen del logo de MUGUI
    - Botones para: Afinador, Metrónomo, Reproductor
    - Callback para cambiar de frame cuando se hace clic en un botón
    """

    def __init__(self, parent, on_tuner_clicked=None, on_metronome_clicked=None,
                 on_reproductor_clicked=None):
        """
        Inicializa el MenuFrame.

        Args:
            parent: Widget padre (tkinter Frame)
            on_tuner_clicked: Callback cuando se hace clic en "Afinador"
            on_metronome_clicked: Callback cuando se hace clic en "Metrónomo"
            on_reproductor_clicked: Callback cuando se hace clic en "Reproductor"
        """
        super().__init__(parent)

        # Guardar callbacks
        self.on_tuner_clicked = on_tuner_clicked
        self.on_metronome_clicked = on_metronome_clicked
        self.on_reproductor_clicked = on_reproductor_clicked

        # Configurar estilo
        self.configure(style='Dark.TFrame')

        # Crear interfaz
        self.setup_ui()

    def setup_ui(self):
        """Configura los elementos de la interfaz de usuario."""
        # Color de fondo
        style = ttk.Style()
        style.configure('Dark.TFrame', background='#1a1a1a')
        style.configure('Welcome.TLabel', background='#1a1a1a', foreground='#ffffff',
                        font=('Arial', 24, 'bold'))
        style.configure('MenuButton.TButton', font=('Arial', 12, 'bold'),
                        width=15)

        # Frame principal con scroll vertical
        main_frame = ttk.Frame(self, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Logo - Más grande
        logo_path = self._get_logo_path()
        if os.path.exists(logo_path):
            self._add_logo(main_frame, logo_path)

        # Descripción
        description_label = ttk.Label(
            main_frame,
            text="Selecciona una función para comenzar",
            style='Welcome.TLabel',
            font=('Arial', 14)
        )
        description_label.pack(pady=10)

        # Frame para botones
        buttons_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        buttons_frame.pack(pady=30)

        # Botones
        self._create_button(
            buttons_frame,
            "🎸 Afinador",
            self.on_tuner_clicked,
            row=0, column=0
        )

        self._create_button(
            buttons_frame,
            "⏱️ Metrónomo",
            self.on_metronome_clicked,
            row=0, column=1
        )

        self._create_button(
            buttons_frame,
            "🎵 Reproductor",
            self.on_reproductor_clicked,
            row=0, column=2
        )

    def _get_logo_path(self):
        """Obtiene la ruta del logo."""
        # Buscar logo.png en la carpeta imagenes
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        logo_path = os.path.join(base_path, 'imagenes', 'logo.png')
        return logo_path

    def _add_logo(self, parent, logo_path):
        """Agrega el logo a la interfaz."""
        try:
            # Cargar imagen
            image = Image.open(logo_path)

            # Redimensionar (más grande: 300x300)
            image.thumbnail((300, 300), Image.Resampling.LANCZOS)

            # Convertir a PhotoImage
            photo = ImageTk.PhotoImage(image)

            # Crear label con imagen
            logo_label = tk.Label(parent, image=photo, bg='#1a1a1a')
            logo_label.image = photo  # Guardar referencia para evitar garbage collection
            logo_label.pack(pady=20)
        except Exception as e:
            print(f"Error cargando logo: {e}")

    def _create_button(self, parent, text, callback, row, column):
        """Crea un botón con estilo."""
        button = ttk.Button(
            parent,
            text=text,
            command=callback,
            style='MenuButton.TButton'
        )
        button.grid(row=row, column=column, padx=15, pady=10)
