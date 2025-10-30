import tkinter
# Code to add widgets will go here...
top = tkinter.Tk()

B = tkinter.Button(top, text="Hello", command=lambda: cambiar_color())


def cambiar_color():
    B.config(background="#da4f30")


B.pack()


top.mainloop()
