# ViewModel del metrónomo: lógica de control, loop en hilo separado y comunicación con la vista vía callbacks.
from typing import Callable, Optional
import threading
import time


class MetronomeViewModel:
    """
    ViewModel para el metrónomo.
    - Recibe un modelo (MetronomeModel) responsable de sonido.
    - Expones métodos para iniciar/parar, setear bpm/compás, tap tempo.
    - Notifica la vista por el callback on_tick(index, accent).
    """

    def __init__(self, model):
        self.model = model
        self.bpm = 120
        self.compas = 4
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._beat_count = 0
        self.on_tick: Optional[Callable[[int, bool], None]] = None  # callback(view): index, accent
        self._tap_times = []

    def set_bpm(self, bpm: int):
        self.bpm = max(20, min(300, int(bpm)))

    def set_compas(self, compas: int):
        self.compas = max(1, min(12, int(compas)))

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        if self.running:
            return
        self.running = True
        self._beat_count = 0
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self.running = False
        # El hilo terminará pronto; no se joinea para no bloquear la UI.

    def _run_loop(self):
        while self.running:
            delay = 60.0 / max(1, self.bpm)
            accent = (self._beat_count % self.compas) == 0
            try:
                # Reproducir sonido (modelo maneja excepciones internas)
                self.model.play_click(accent)
            except Exception:
                pass
            # Notificar a la vista (si existe callback)
            if self.on_tick:
                try:
                    self.on_tick(self._beat_count % self.compas, accent)
                except Exception:
                    pass
            self._beat_count += 1
            # Dormir (no usar busy-wait)
            time.sleep(delay)

    def tap(self):
        """Agregar un golpe en Tap Tempo; si hay suficientes entries calcula bpm medio."""
        now = time.time()
        # mantener taps recientes (2 segundos)
        self._tap_times = [t for t in self._tap_times if now - t < 2.0] + [now]
        if len(self._tap_times) >= 3:
            diffs = [self._tap_times[i+1] - self._tap_times[i] for i in range(len(self._tap_times)-1)]
            if diffs:
                avg = sum(diffs) / len(diffs)
                bpm = int(60.0 / avg)
                if 20 <= bpm <= 300:
                    self.set_bpm(bpm)
                    return bpm
        return None