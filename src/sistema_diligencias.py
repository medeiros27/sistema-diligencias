#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface gráfica com Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config import WINDOW_TITLE, WINDOW_SIZE, COLORS


class SistemaDiligencias:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self._build_ui()

    def _build_ui(self):
        # Exemplo simples: apenas uma aba
        notebook = ttk.Notebook(self.root)
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Diligências")
        notebook.pack(expand=True, fill="both")

        lbl = ttk.Label(frame, text="Bem-vindo ao Sistema de Diligências")
        lbl.pack(pady=20)

    def run(self):
        self.root.mainloop()