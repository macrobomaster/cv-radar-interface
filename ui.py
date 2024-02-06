from tkinter import *
from tkinter import ttk


class UI:

    def __init__(self, arena_map, camera_feed):
        self.root = Tk()
        self.frm = ttk.Frame(radar, padding=10)
        self.frm.grid()
        self.ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
        self.ttk.Button(frm, text="Quit", command=root.destroy).grid(column=2, row=0)
        self.ttk.Label(frm, text="Yeehaw").grid(column=1, row=0)
        self.frm.update_idletasks()
        self.frm.update()