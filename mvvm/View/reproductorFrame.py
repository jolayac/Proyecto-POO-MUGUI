import tkinter as tk
from tkinter import Frame
from mvvm.ViewModel.reproductor_vm import ReproductorViewModel
from mvvm.View.reproductorView.reproductorUI import VistaReproductor


class ReproductorFrame(Frame):
    """
    Frame embebible que contiene el reproductor de música.
    Se integra dentro de la ventana principal de MainApp.
    """

    def __init__(self, master=None):
        super().__init__(master, bg="black")

        # Crear el ViewModel del reproductor
        self.vm = ReproductorViewModel()

        # Crear la vista del reproductor dentro de este Frame
        self.vista = VistaReproductor(self, self.vm)
