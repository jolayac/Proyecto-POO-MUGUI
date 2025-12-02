# Vista del metrónomo (Frame embebible). Se conecta a MetronomeViewModel.
import tkinter as tk
from tkinter import ttk, messagebox

from mvvm.Model.MetronomeModel import MetronomeModel
from mvvm.ViewModel.MetronomeVM import MetronomeViewModel

# Paleta recomendada (fondo oscuro y colores contrastantes)
_BG = "#1b1b1b"
_PANEL = "#323232"
_ACCENT = "#FC6E20"
_HIGHLIGHT = "#fee8d0"


class MetronomeFrame(ttk.Frame):
    """
    Frame embebible que implementa la interfaz del metrónomo.
    - Se puede instanciar dentro de la ventana principal (MainApp) o en un Toplevel.
    - Conecta con MetronomeViewModel y actualiza la UI mediante after()-safe callbacks.
    - Los círculos se ajustan dinámicamente según el compás seleccionado.
    """

    def __init__(self, master=None):
        super().__init__(master)
        # Estilos mínimos
        self.master = master
        self.configure(style="Metronome.TFrame")
        # Modelo + VM
        self.model = MetronomeModel()
        self.vm = MetronomeViewModel(self.model)
        self.vm.on_tick = self._on_tick  # callback desde VM

        # Estado UI
        self._lights = []
        self._lights_frame = None
        self._create_ui()

    def _create_ui(self):
        self.pack_propagate(False)

        # Configure a dark style for ttk widgets
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Metronome.TFrame", background=_BG)
        style.configure("Title.TLabel", background=_BG, foreground=_HIGHLIGHT, font=("Arial", 18, "bold"))
        style.configure("Big.TLabel", background=_BG, foreground=_HIGHLIGHT, font=("Consolas", 48, "bold"))
        style.configure("Accent.TButton", background=_ACCENT, foreground="black")
        style.map("Accent.TButton", background=[("active", "#ff8a42")])

        # Main container
        container = tk.Frame(self, bg=_BG)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(container, text="Metrónomo", font=("Arial", 20, "bold"),
                 fg=_HIGHLIGHT, bg=_BG).pack(pady=(6, 12))

        # BPM display
        self.bpm_label = tk.Label(container, text=str(self.vm.bpm),
                                  font=("Consolas", 40, "bold"),
                                  fg=_HIGHLIGHT, bg=_BG)
        self.bpm_label.pack(pady=(6, 8))

        # Slider BPM
        frame_slider = tk.Frame(container, bg=_BG)
        frame_slider.pack(pady=(6, 8))
        tk.Label(frame_slider, text="BPM", bg=_BG, fg="#cccccc").pack(side="left", padx=(0, 8))
        self.slider = ttk.Scale(frame_slider, from_=20, to=300, orient="horizontal",
                                length=300, command=self._on_slider)
        self.slider.set(self.vm.bpm)
        self.slider.pack(side="left")

        # Entry BPM
        self.entry_bpm = tk.Entry(container, width=6, justify="center")
        self.entry_bpm.insert(0, str(self.vm.bpm))
        self.entry_bpm.pack(pady=6)
        self.entry_bpm.bind("<Return>", lambda e: self._on_entry())

        # Compas combobox
        tk.Label(container, text="Compás", bg=_BG, fg="#cccccc").pack(pady=(8, 2))
        self.compas_var = tk.StringVar(value=str(self.vm.compas))
        combo = ttk.Combobox(container, textvariable=self.compas_var, 
                             values=[str(i) for i in range(1, 13)], width=4, state="readonly")
        combo.pack()
        combo.bind("<<ComboboxSelected>>", lambda e: self._on_compas())

        # Lights (visual beat indicators) - frame que se recreará al cambiar compás
        self._lights_frame = tk.Frame(container, bg=_BG)
        self._lights_frame.pack(pady=12)
        self._recreate_lights()

        # Controls
        controls = tk.Frame(container, bg=_BG)
        controls.pack(pady=12)
        self.btn_toggle = tk.Button(controls, text="INICIAR", bg=_ACCENT, fg="black", 
                                    width=12, command=self._on_toggle)
        self.btn_toggle.pack(side="left", padx=6)
        tk.Button(controls, text="−10", bg=_PANEL, fg="white", 
                 command=lambda: self._on_adjust(-10)).pack(side="left", padx=4)
        tk.Button(controls, text="+10", bg=_PANEL, fg="white", 
                 command=lambda: self._on_adjust(10)).pack(side="left", padx=4)

        # Tap tempo
        tk.Label(container, text="TAP TEMPO", bg=_BG, fg="#bbbbbb").pack(pady=(10, 0))
        tk.Button(container, text="TAP", width=10, bg=_HIGHLIGHT, fg="black", 
                 command=self._on_tap).pack(pady=6)

        # Status
        '''
        status_text = "Sonido: pygame" if self.model.using_pygame else (
            "Sonido: winsound" if self.model.has_winsound else "Sonido: sistema")
        color = "#00ff00" if self.model.using_pygame else "#ffaa00"
        self.status_label = tk.Label(container, text=status_text, bg=_BG, fg=color)
        self.status_label.pack(pady=(8, 0))
        '''

    def _recreate_lights(self):
        """Recrear los círculos según el compás actual."""
        # Limpiar los anteriores
        for c in self._lights:
            c.destroy()
        self._lights = []

        # Crear nuevos círculos según el compás
        comp = self.vm.compas
        for i in range(comp):
            c = tk.Canvas(self._lights_frame, width=40, height=40, bg=_BG, highlightthickness=0)
            circ = c.create_oval(6, 6, 34, 34, fill="#333333", outline="#555555", width=3)
            c.circ_id = circ
            c.pack(side="left", padx=6)
            self._lights.append(c)

    # ---- UI callbacks que invocan el VM ----
    def _on_slider(self, val):
        bpm = int(float(val))
        self.vm.set_bpm(bpm)
        self.bpm_label.config(text=str(bpm))
        self.entry_bpm.delete(0, tk.END)
        self.entry_bpm.insert(0, str(bpm))

    def _on_entry(self):
        try:
            v = int(self.entry_bpm.get())
            self.vm.set_bpm(v)
            self.slider.set(v)
            self.bpm_label.config(text=str(v))
        except Exception:
            pass

    def _on_compas(self):
        try:
            c = int(self.compas_var.get())
            self.vm.set_compas(c)
            # Recrear los círculos cuando cambia el compás
            self._recreate_lights()
        except Exception:
            pass

    def _on_toggle(self):
        self.vm.toggle()
        # actualizar texto del botón según nuevo estado
        if self.vm.running:
            self.btn_toggle.config(text="PARAR", bg="#ff3333", fg="white")
        else:
            self.btn_toggle.config(text="INICIAR", bg=_ACCENT, fg="black")
            # limpiar luces cuando se para
            self._clear_lights()

    def _on_adjust(self, delta: int):
        self.vm.set_bpm(self.vm.bpm + delta)
        self.slider.set(self.vm.bpm)
        self.bpm_label.config(text=str(self.vm.bpm))
        self.entry_bpm.delete(0, tk.END)
        self.entry_bpm.insert(0, str(self.vm.bpm))

    def _on_tap(self):
        bpm = self.vm.tap()
        if bpm:
            # reflejar nuevo BPM en UI
            self.slider.set(bpm)
            self.bpm_label.config(text=str(bpm))
            self.entry_bpm.delete(0, tk.END)
            self.entry_bpm.insert(0, str(bpm))

    # ---- callback llamado por el VM (puede ejecutarse en hilo distinto) ----
    def _on_tick(self, idx: int, accent: bool):
        # Asegurar que la actualización UI se ejecute en hilo principal
        try:
            self.after(0, self._highlight, idx, accent)
        except Exception:
            pass

    def _highlight(self, idx: int, accent: bool):
        # Actualizar solo hasta compás actual (dinámico según self._lights)
        for i, c in enumerate(self._lights):
            color = "#ff3333" if (i == idx and accent) else ("#4488ff" if i == idx else "#333333")
            c.itemconfig(c.circ_id, fill=color)

    def _clear_lights(self):
        for c in self._lights:
            c.itemconfig(c.circ_id, fill="#333333")


# Launcher seguro para ejecutar el metrónomo como ventana independiente.
def lanzar_metronomo():
    try:
        root = tk.Tk()
        root.title("Metrónomo - MUGUI")
        root.geometry("820x520")
        root.configure(bg=_BG)
        frame = MetronomeFrame(root)
        frame.pack(fill="both", expand=True)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el metrónomo:\n{e}")


# Permitir ejecución directa del archivo
if __name__ == "__main__":
    lanzar_metronomo()