class TimeBarController:
    '''Controlador para la barra de tiempo. Maneja la interacción del usuario y la actualización del valor.'''
    def __init__(self, scale_widget, vm):
        self.scale = scale_widget
        self.vm = vm
        self._user_dragging = False
        self._last_set = 0
        self._last_seek = 0

    def set_value(self, value):
        
        if not self._user_dragging:
            self.scale.set(value)
            self._last_set = value

    def on_seek_start(self, event=None):
        self._user_dragging = True

    def on_seek_end(self, event=None):
        self._user_dragging = False
        self._last_seek = self.scale.get()
        self.seek_to(self._last_seek)

    def seek_to(self, value):
        total = self.vm.track_length()
        if total > 0:
            try:
                import pygame
                pygame.mixer.music.pause()
                pygame.mixer.music.set_pos(float(value))
                pygame.mixer.music.unpause()
            except Exception:
                try:
                    pygame.mixer.music.play(start=float(value))
                except Exception:
                    return
