# metronomo.py
# METRÓNOMO MUGUI - VERSIÓN FINAL 100% FUNCIONAL Y SIN ERRORES

import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import numpy as np
import sys

# ==============================================
# INTENTAR PYGAME (mejor calidad)
# ==============================================
try:
    import pygame
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=256)
    pygame.mixer.init()
    USANDO_PYGAME = True
    print("[METRÓNOMO] → Usando pygame (sonido de alta calidad)")
except Exception as e:
    USANDO_PYGAME = False
    print(f"[METRÓNOMO] pygame falló: {e}")

if not USANDO_PYGAME and sys.platform.startswith('win'):
    import winsound

class MetronomoApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Metrónomo - MUGUI")
        self.root.geometry("520x820")   # ← Tamaño IDEAL y bonito
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.bpm = 120
        self.corriendo = False
        self.beat_count = 0
        self.compas = 4
        self.tap_times = []

        # SONIDOS (solo si pygame funciona)
        if USANDO_PYGAME:
            self.click_acento = self._crear_sonido(1000, 0.08, 0.8)
            self.click_normal = self._crear_sonido(800, 0.06, 0.5)
        else:
            self.click_acento = self.click_normal = None

        # CREAR INTERFAZ (todo después de __init__)
        self._crear_interfaz()

    def _crear_sonido(self, freq, duracion, volumen):
        try:
            fs = 44100
            t = np.linspace(0, duracion, int(fs * duracion), False)
            onda = np.sin(2 * np.pi * freq * t) * volumen
            onda = np.int16(onda * 32767)
            return pygame.sndarray.make_sound(onda)
        except:
            return None

    def reproducir_click(self, acento=False):
        if USANDO_PYGAME and (acento and self.click_acento or not acento and self.click_normal):
            try:
                (self.click_acento if acento else self.click_normal).play()
                return
            except:
                pass

        if sys.platform.startswith('win'):
            try:
                freq = 1000 if acento else 800
                dur = 120 if acento else 80
                winsound.Beep(freq, dur)
            except:
                pass
        else:
            print("\a", end="")

    def _crear_interfaz(self):
        # Título
        tk.Label(self.root, text="METRÓNOMO", font=("Arial", 28, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=30)

        # BPM grande
        self.bpm_label = tk.Label(self.root, text="120", font=("Consolas", 80, "bold"),
                                  fg="white", bg="#1e1e1e")
        self.bpm_label.pack(pady=20)

        # Slider BPM
        tk.Label(self.root, text="BPM", font=("Arial", 14), fg="#ffffff", bg="#1e1e1e").pack()
        self.slider = ttk.Scale(self.root, from_=40, to=240, orient="horizontal",
                                length=320, command=self._actualizar_desde_slider)
        self.slider.set(120)
        self.slider.pack(pady=12)

        # Entrada manual BPM
        self.entry_bpm = tk.Entry(self.root, font=("Arial", 16), width=6, justify="center")
        self.entry_bpm.insert(0, "120")
        self.entry_bpm.pack(pady=5)
        self.entry_bpm.bind("<Return>", lambda e: self._actualizar_desde_entry())

        # Compás
        tk.Label(self.root, text="Compás", font=("Arial", 12), fg="#aaaaaa", bg="#1e1e1e").pack(pady=(20,5))
        self.compas_var = tk.StringVar(value="4")
        combo = ttk.Combobox(self.root, textvariable=self.compas_var,
                             values=["2","3","4","5","6","7"], width=5, state="readonly")
        combo.pack()
        self.compas_var.trace("w", lambda *_: self._actualizar_compas())

        # Luces
        self.luces_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.luces_frame.pack(pady=30)
        self.luces = []
        for i in range(7):
            c = tk.Canvas(self.luces_frame, width=62, height=62, bg="#1e1e1e", highlightthickness=0)
            circ = c.create_oval(8, 8, 54, 54, fill="#333333", outline="#555555", width=4)
            c.pack(side="left", padx=14)
            c.circ_id = circ
            self.luces.append(c)

        # Botones
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=30)

        self.btn_play = tk.Button(btn_frame, text="INICIAR", font=("Arial", 16, "bold"),
                                  bg="#fc6e20", fg="black", width=12, height=2,
                                  command=self.toggle)
        self.btn_play.pack(side="left", padx=20)

        tk.Button(btn_frame, text="−10", font=("Arial", 16), bg="#323232", fg="white",
                  command=lambda: self.ajustar(-10)).pack(side="left", padx=10)
        tk.Button(btn_frame, text="+10", font=("Arial", 16), bg="#323232", fg="black",
                  command=lambda: self.ajustar(10)).pack(side="left", padx=10)

        # Tap Tempo
        tk.Label(self.root, text="TAP TEMPO", font=("Arial", 10), fg="#888888", bg="#1e1e1e").pack(pady=(25,0))
        tk.Button(self.root, text="TAP", font=("Arial", 20, "bold"), width=10, height=2,
                  bg="#ffff55", fg="black", command=self.tap_tempo).pack(pady=10)

        # Estado de sonido
        estado = "Sonido: pygame" if USANDO_PYGAME else "Sonido: sistema"
        color = "#00ff00" if USANDO_PYGAME else "#ffaa00"
        tk.Label(self.root, text=estado, font=("Arial", 9), fg=color, bg="#1e1e1e").pack(pady=5)

    def _actualizar_desde_slider(self, val):
        valor = int(float(val))
        self.bpm = valor
        self.bpm_label.config(text=str(valor))
        if hasattr(self, 'entry_bpm'):
            self.entry_bpm.delete(0, tk.END)
            self.entry_bpm.insert(0, str(valor))

    def _actualizar_desde_entry(self):
        try:
            valor = int(self.entry_bpm.get())
            if 40 <= valor <= 240:
                self.bpm = valor
                self.bpm_label.config(text=str(valor))
                self.slider.set(valor)
        except:
            pass

    def _actualizar_compas(self):
        self.compas = int(self.compas_var.get())

    def ajustar(self, delta):
        nuevo = max(40, min(240, self.bpm + delta))
        self.bpm = nuevo
        self.bpm_label.config(text=str(nuevo))
        self.slider.set(nuevo)
        self.entry_bpm.delete(0, tk.END)
        self.entry_bpm.insert(0, str(nuevo))

    def tap_tempo(self):
        ahora = time.time()
        self.tap_times = [t for t in self.tap_times if ahora - t < 2.0] + [ahora]
        if len(self.tap_times) >= 3:
            diffs = np.diff(self.tap_times)
            if len(diffs) > 0:
                bpm = int(60 / np.mean(diffs))
                if 40 <= bpm <= 240:
                    self.ajustar(bpm - self.bpm)  # Usa ajustar para mantener sincronía

    def toggle(self):
        if self.corriendo:
            self.corriendo = False
            self.btn_play.config(text="INICIAR", bg="#fc6e20", fg="black")
        else:
            self.corriendo = True
            self.btn_play.config(text="PARAR", bg="#ff0000", fg="white")
            self.beat_count = 0
            threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self.corriendo:
            delay = 60.0 / self.bpm
            acento = self.beat_count % self.compas == 0
            self.reproducir_click(acento)
            color = "#ff3333" if acento else "#4488ff"
            self.root.after(0, self._iluminar, self.beat_count % self.compas, color)
            self.beat_count += 1
            time.sleep(delay)

    def _iluminar(self, idx, color):
        for i, canvas in enumerate(self.luces):
            canvas.itemconfig(canvas.circ_id, fill=color if i == idx else "#333333")

    def run(self):
        self.root.mainloop()


# LANZADOR SEGURO
def lanzar_metronomo():
    try:
        app = MetronomoApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el metrónomo:\n{e}")


if __name__ == "__main__":
    lanzar_metronomo()