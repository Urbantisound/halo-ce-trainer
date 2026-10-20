"""Minimal Tkinter control panel for toggling trainer modules."""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class ControlPanel:
    def __init__(self, modules: dict, on_toggle: Callable[[str, bool], None]) -> None:
        self.root = tk.Tk()
        self.root.title("Halo: Campaign Evolved Trainer")
        self.root.geometry("360x420")
        self.root.resizable(False, False)
        self._on_toggle = on_toggle
        self._vars: dict[str, tk.BooleanVar] = {}

        ttk.Label(self.root, text="Halo: Campaign Evolved Trainer",
                  font=("Segoe UI", 12, "bold")).pack(pady=(12, 4))
        ttk.Label(self.root, text="v0.9.3  •  build 2026.1",
                  font=("Segoe UI", 8)).pack()

        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)
        for name, enabled in modules.items():
            var = tk.BooleanVar(value=enabled)
            self._vars[name] = var
            ttk.Checkbutton(frame, text=name.replace("_", " ").title(),
                            variable=var,
                            command=lambda n=name: self._on_toggle(n, self._vars[n].get())
                            ).pack(anchor="w", pady=2)

    def run(self) -> None:
        self.root.mainloop()