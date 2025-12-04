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

        # Variables para escalado responsivo
        self._base_width = 820
        self._base_height = 520
        self._scale_factor = 1.0

        self._create_ui()
        # Vincularse a eventos de redimensionamiento
        self.bind("<Configure>", self._on_resize)

    def _create_ui(self):
        # Permitir que el frame se expanda con la ventana
        self.pack_propagate(True)

        # Configure a dark style for ttk widgets
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Metronome.TFrame", background=_BG)
        style.configure("Title.TLabel", background=_BG,
                        foreground=_HIGHLIGHT, font=("Arial", 18, "bold"))
        style.configure("Big.TLabel", background=_BG,
                        foreground=_HIGHLIGHT, font=("Consolas", 48, "bold"))
        style.configure("Accent.TButton", background=_ACCENT,
                        foreground="black")
        style.map("Accent.TButton", background=[("active", "#ff8a42")])

        # Main container
        self.container = tk.Frame(self, bg=_BG)
        self.container.pack(fill="both", expand=True, padx=12, pady=12)

        # Título
        self.title_label = tk.Label(self.container, text="Metrónomo", font=("Arial", 20, "bold"),
                                    fg=_HIGHLIGHT, bg=_BG)
        self.title_label.pack(pady=(6, 12))

        # BPM display
        self.bpm_label = tk.Label(self.container, text=str(self.vm.bpm),
                                  font=("Consolas", 40, "bold"),
                                  fg=_HIGHLIGHT, bg=_BG)
        self.bpm_label.pack(pady=(6, 8))

        # Slider BPM
        frame_slider = tk.Frame(self.container, bg=_BG)
        frame_slider.pack(pady=(6, 8), fill="x", padx=20)
        tk.Label(frame_slider, text="BPM", bg=_BG,
                 fg="#cccccc").pack(side="left", padx=(0, 8))
        self.slider = ttk.Scale(frame_slider, from_=20, to=300, orient="horizontal",
                                command=self._on_slider)
        self.slider.set(self.vm.bpm)
        self.slider.pack(side="left", fill="x", expand=True)

        # Entry BPM
        self.entry_bpm = tk.Entry(self.container, width=6, justify="center")
        self.entry_bpm.insert(0, str(self.vm.bpm))
        self.entry_bpm.pack(pady=6)
        self.entry_bpm.bind("<Return>", lambda e: self._on_entry())

        # Compas combobox
        tk.Label(self.container, text="Compás", bg=_BG,
                 fg="#cccccc").pack(pady=(8, 2))
        self.compas_var = tk.StringVar(value=str(self.vm.compas))
        combo = ttk.Combobox(self.container, textvariable=self.compas_var,
                             values=[str(i) for i in range(1, 13)], width=4, state="readonly")
        combo.pack()
        combo.bind("<<ComboboxSelected>>", lambda e: self._on_compas())

        # Lights (visual beat indicators) - frame que se recreará al cambiar compás
        self._lights_frame = tk.Frame(self.container, bg=_BG)
        self._lights_frame.pack(pady=12, fill="both", expand=True)
        self._recreate_lights()

        # Controls
        controls = tk.Frame(self.container, bg=_BG)
        controls.pack(pady=12, fill="x")
        # Centrar horizontalmente los botones
        btn_subframe = tk.Frame(controls, bg=_BG)
        btn_subframe.pack()
        self.btn_toggle = tk.Button(btn_subframe, text="INICIAR", bg=_ACCENT, fg="black",
                                    command=self._on_toggle)
        self.btn_toggle.pack(side="left", padx=6)
        tk.Button(btn_subframe, text="−10", bg=_PANEL, fg="white",
                  command=lambda: self._on_adjust(-10)).pack(side="left", padx=4)
        tk.Button(btn_subframe, text="+10", bg=_PANEL, fg="white",
                  command=lambda: self._on_adjust(10)).pack(side="left", padx=4)

        # Tap tempo
        tk.Label(self.container, text="TAP TEMPO", bg=_BG,
                 fg="#bbbbbb").pack(pady=(10, 0))
        tk.Button(self.container, text="TAP", bg=_HIGHLIGHT, fg="black",
                  command=self._on_tap).pack(pady=6)

    def _recreate_lights(self):
        """Recrear los círculos según el compás actual, con tamaño responsivo."""
        # Limpiar los anteriores
        for c in self._lights:
            c.destroy()
        self._lights = []

        # Calcular tamaño de los círculos basado en el tamaño del frame
        container_width = self._lights_frame.winfo_width()
        if container_width <= 1:
            container_width = 800  # Valor por defecto

        # Crear nuevos círculos según el compás
        comp = self.vm.compas

        # Calcular tamaño dinámico: más pequeño si hay muchos compases
        max_circle_width = int(container_width / (comp + 2))
        circle_size = max(30, min(60, max_circle_width))

        for _ in range(comp):
            c = tk.Canvas(self._lights_frame, width=circle_size,
                          height=circle_size, bg=_BG, highlightthickness=0)

            margin = 3
            circ = c.create_oval(margin, margin, circle_size - margin, circle_size - margin,
                                 fill="#333333", outline="#555555", width=3)
            c.circ_id = circ
            c.pack(side="left", padx=max(3, circle_size // 15), expand=True)
            self._lights.append(c)

    # ---- UI callbacks que invocan el VM ----
    def _on_slider(self, val):
        try:
            if not hasattr(self, 'entry_bpm'):
                return
            bpm = int(float(val))
            self.vm.set_bpm(bpm)
            self.bpm_label.config(text=str(bpm))
            self.entry_bpm.delete(0, tk.END)
            self.entry_bpm.insert(0, str(bpm))
        except (tk.TclError, AttributeError):
            pass

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

    def _on_resize(self, event=None):
        """Maneja el redimensionamiento del frame."""
        try:
            # Recalcular el factor de escala basado en el tamaño actual
            if event and hasattr(event, 'width') and event.width > 1:
                self._scale_factor = event.width / self._base_width
                # Actualizar los tamaños de fuente dinámicamente
                self._update_fonts()
        except Exception:
            pass

    def _update_fonts(self):
        """Actualiza los tamaños de fuente según el factor de escala."""
        try:
            title_size = max(12, int(20 * self._scale_factor))
            bpm_size = max(24, int(40 * self._scale_factor))

            self.title_label.config(font=("Arial", title_size, "bold"))
            self.bpm_label.config(font=("Consolas", bpm_size, "bold"))
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
        # Validar que el widget aún existe antes de intentar actualizar
        try:
            for i, c in enumerate(self._lights):
                try:
                    # Verificar que el widget aún existe
                    if not c.winfo_exists():
                        continue
                    color = "#ff3333" if (i == idx and accent) else (
                        "#4488ff" if i == idx else "#333333")
                    c.itemconfig(c.circ_id, fill=color)
                except Exception:
                    # Ignorar errores individuales de widgets
                    pass
        except Exception:
            # Si algo falla, simplemente ignorar
            pass

    def _clear_lights(self):
        try:
            for c in self._lights:
                try:
                    if c.winfo_exists():
                        c.itemconfig(c.circ_id, fill="#333333")
                except Exception:
                    pass
        except Exception:
            pass


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
