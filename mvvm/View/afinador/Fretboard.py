from tkinter import Canvas, Frame



class FretboardFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#222222")
        self.canvas = Canvas(self, width=600, height=320,
                             bg="#222222", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self.draw_fretboard()
        self.note_boxes = []
        self.last_positions = []

    def draw_fretboard(self):
        self.canvas.delete("all")
        # Dibujar cuerdas
        for i in range(6):
            y = 40 + i*40
            self.canvas.create_line(40, y, 560, y, fill="#aaa", width=2)
        # Dibujar trastes
        for fret in range(20):
            x = 40 + fret*27
            self.canvas.create_line(x, 40, x, 240, fill="#888", width=1)
            if fret > 0:
                self.canvas.create_text(x, 250, text=str(
                    fret), fill="#ccc", font=("Arial", 9))

    def update_notes(self, positions):
        # Mantener las últimas posiciones si no hay nuevas
        if positions:
            self.last_positions = positions
        self.draw_fretboard()
        # Marcar posiciones de la nota
        for string, fret in self.last_positions:
            x = 40 + fret*27
            y = 40 + (string-1)*40
            self.canvas.create_rectangle(
                x-10, y-10, x+10, y+10, fill="#00ff88", outline="#005544", width=2)
            self.canvas.create_text(
                x, y, text="●", fill="#222", font=("Arial", 12, "bold"))