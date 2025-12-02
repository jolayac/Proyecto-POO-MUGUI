from tkinter import Frame, Label, Button, PhotoImage, ttk
from mvvm.View.reproductorView.barra_de_tiempo import TimeBarController
import os
import sys


class VistaReproductor:
    """
    Vista principal del reproductor de música.
    Contiene la interfaz gráfica y conecta los controles con el ViewModel.
    """

    def __init__(self, raiz, viewmodel):
        self.raiz = raiz
        self.vm = viewmodel

        # Solo configurar si raiz es una ventana Tk (no un Frame)
        if hasattr(self.raiz, 'title'):
            try:
                self.raiz.title('Reproductor de Música')
            except:
                pass

        if hasattr(self.raiz, 'iconbitmap'):
            try:
                self.raiz.iconbitmap('icono.ico')
            except (OSError, Exception):
                try:
                    self.raiz.iconbitmap('')
                except:
                    pass

        if hasattr(self.raiz, 'config'):
            try:
                self.raiz.config(bg='black')
            except:
                pass

        if hasattr(self.raiz, 'resizable'):
            try:
                self.raiz.resizable(1, 1)
            except:
                pass

        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure("Horizontal.TScale", bordercolor='#FC6E20', troughcolor='black',
                         background='#FC6E20', foreground='#FC6E20', lightcolor='#FC6E20', darkcolor='black')

        # Contenedor central que usa pack en lugar de grid para mejor centrado
        contenedor_central = Frame(self.raiz, bg='black')
        contenedor_central.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame superior con barra de tiempo y controles
        self.marco_superior = Frame(contenedor_central, bg='black')
        self.marco_superior.pack(fill="x", padx=5, pady=(5, 10))

        # Barra de tiempo arriba
        frame_tiempo = Frame(self.marco_superior, bg='black')
        frame_tiempo.pack(fill="x", pady=(0, 5))

        self.barra_tiempo = ttk.Scale(frame_tiempo, from_=0, to=100, orient='horizontal',
                                      style='Horizontal.TScale')
        self.barra_tiempo.pack(side="left", fill="x", expand=True)

        self.texto_tiempo = Label(
            frame_tiempo, bg='black', fg='#FC6E20', width=10)
        self.texto_tiempo.pack(side="left", padx=(5, 0))

        self.control_tiempo = TimeBarController(self.barra_tiempo, self.vm)
        self.barra_tiempo.bind('<Button-1>', self.control_tiempo.on_seek_start)
        self.barra_tiempo.bind('<ButtonRelease-1>',
                               self.control_tiempo.on_seek_end)

        # Nombre de la pista
        self.etiqueta_nombre = Label(
            self.marco_superior, bg='black', fg='#FC6E20', wraplength=350)
        self.etiqueta_nombre.pack(fill="x", pady=(0, 5))

        self.etiqueta_cantidad = Label(
            self.marco_superior, bg='black', fg='#FC6E20', font=("Arial", 9))
        self.etiqueta_cantidad.pack(anchor="e")

        # Carga de imágenes de los botones
        self.imagen_carpeta = self._cargar_imagen('carpeta.png')
        self.imagen_play = self._cargar_imagen('play.png')
        self.imagen_pausa = self._cargar_imagen('pausa.png')
        self.imagen_repetir = self._cargar_imagen('repetir.png')
        self.imagen_stop = self._cargar_imagen('stop.png')
        self.imagen_anterior = self._cargar_imagen('anterior.png')
        self.imagen_adelante = self._cargar_imagen('adelante.png')

        # Frame de botones
        frame_botones = Frame(self.marco_superior, bg='black')
        frame_botones.pack(pady=(5, 0))

        # Botones de control
        self.boton_carpeta = Button(frame_botones, image=self.imagen_carpeta, command=self.abrir_archivos,
                                    borderwidth=0, highlightthickness=0, bg='black', activebackground='black')
        self.boton_carpeta.pack(side="left", padx=2)

        self.boton_play = Button(frame_botones, image=self.imagen_play, command=self.reproducir,
                                 borderwidth=0, highlightthickness=0, bg='black', activebackground='black')
        self.boton_play.pack(side="left", padx=2)

        self.boton_stop = Button(frame_botones, image=self.imagen_stop, command=self.detener,
                                 borderwidth=0, highlightthickness=0, bg='black', activebackground='black')
        self.boton_stop.pack(side="left", padx=2)

        self.boton_pausa = Button(frame_botones, image=self.imagen_pausa, command=self.pausar,
                                  borderwidth=0, highlightthickness=0, bg='black', activebackground='black')
        self.boton_pausa.pack(side="left", padx=2)

        self.boton_continuar = Button(frame_botones, image=self.imagen_repetir, command=self.continuar,
                                      borderwidth=0, highlightthickness=0, bg='black', activebackground='black')
        self.boton_continuar.pack(side="left", padx=2)

        self.boton_anterior = Button(frame_botones, image=self.imagen_anterior, command=self.anterior,
                                     borderwidth=0, highlightthickness=0, bg='black', activebackground='black')
        self.boton_anterior.pack(side="left", padx=2)

        self.boton_adelante = Button(frame_botones, image=self.imagen_adelante, command=self.siguiente,
                                     borderwidth=0, highlightthickness=0, bg='black', activebackground='black')
        self.boton_adelante.pack(side="left", padx=2)

        # Frame volumen
        frame_volumen = Frame(self.marco_superior, bg='black')
        frame_volumen.pack(pady=(5, 0), anchor="center")

        Label(frame_volumen, text="Vol:", bg='black',
              fg='#FC6E20').pack(side="left", padx=(0, 5))

        self.barra_volumen = ttk.Scale(frame_volumen, to=10, from_=0, orient='horizontal',
                                       length=100, command=self.cambiar_volumen, style='Horizontal.TScale')
        self.barra_volumen.pack(side="left", padx=(0, 5))
        self.barra_volumen.set(10)

        # Actualiza la UI cada 100ms
        if hasattr(self.vm, 'agregar_callback_actualizacion'):
            self.vm.agregar_callback_actualizacion(self.actualizar_ui)

    def _cargar_imagen(self, nombre):
        """Busca y carga una imagen desde las carpetas posibles."""
        # Detectar si estamos en ejecutable de PyInstaller
        if getattr(sys, 'frozen', False):
            # En ejecutable: sys._MEIPASS es la carpeta del bundle
            base_path = sys._MEIPASS
        else:
            # En desarrollo: usar la carpeta del proyecto
            base_path = os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.dirname(__file__))))

        # Intentar carpetas posibles
        carpetas_relativas = ['imagenes', 'images', 'img', 'imágenes', '']
        for carpeta in carpetas_relativas:
            if carpeta:
                ruta = os.path.join(base_path, carpeta, nombre)
            else:
                ruta = os.path.join(base_path, nombre)

            if os.path.exists(ruta):
                try:
                    return PhotoImage(file=ruta)
                except Exception:
                    return None

        return None

    def abrir_archivos(self):
        """Abre el diálogo para seleccionar archivos de audio."""
        ok = self.vm.abrir_archivos()
        if ok:
            pista = self.vm.pista_actual()
            if pista:
                self.etiqueta_nombre['text'] = pista.nombre
            self.etiqueta_cantidad[
                'text'] = f"{self.vm.modelo.indice_actual+1}/{len(self.vm.modelo.pistas)}"

    def reproducir(self):
        """Reproduce desde la posición actual de la barra de tiempo."""
        pos = self.barra_tiempo.get()
        total = self.vm.duracion_pista()
        if total > 0:
            try:
                import pygame
                pygame.mixer.music.stop()
                self.vm.modelo.cargar_actual()
                pygame.mixer.music.play(start=float(pos))
            except Exception:
                self.vm.reproducir()
        else:
            self.vm.reproducir()

    def pausar(self):
        """Pausa la reproducción."""
        self.vm.pausar()

    def detener(self):
        """Detiene la reproducción."""
        self.vm.detener()

    def continuar(self):
        """Continúa la reproducción pausada."""
        self.vm.continuar()

    def siguiente(self):
        """Avanza a la siguiente pista."""
        self.vm.siguiente()

    def anterior(self):
        """Retrocede a la pista anterior."""
        self.vm.anterior()

    def cambiar_volumen(self, valor):
        """Cambia el volumen de reproducción."""
        self.vm.establecer_volumen(float(valor))

    def actualizar_ui(self):
        """Actualiza la barra de tiempo, el texto de tiempo y el nombre de la pista."""
        total = self.vm.duracion_pista()
        pos = self.vm.posicion_reproduccion_segundos()
        pista = self.vm.pista_actual()
        if pista:
            self.etiqueta_nombre['text'] = pista.nombre
        else:
            self.etiqueta_nombre['text'] = "Sin pista"

        # Actualizar número de pista (actual/total)
        try:
            total_pistas = len(self.vm.modelo.pistas)
            indice = self.vm.modelo.indice_actual
            if total_pistas > 0:
                self.etiqueta_cantidad['text'] = f"{indice+1}/{total_pistas}"
            else:
                self.etiqueta_cantidad['text'] = "0/0"
        except Exception:
            self.etiqueta_cantidad['text'] = "0/0"

        # Actualizar barra de tiempo
        if total > 0:
            self.barra_tiempo.configure(to=total)
            self.control_tiempo.set_value(pos)
            minutos, segundos = divmod(pos, 60)
            minutos_total, segundos_total = divmod(total, 60)
            self.texto_tiempo['text'] = f"{minutos:02d}:{segundos:02d} / {minutos_total:02d}:{segundos_total:02d}"
        else:
            self.barra_tiempo.configure(to=100)
            self.control_tiempo.set_value(0)
            self.texto_tiempo['text'] = "00:00 / 00:00"

    # La funcionalidad de seek ahora está en TimeBarController
