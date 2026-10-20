"""Global hotkey listener using Win32 RegisterHotKey."""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import threading
from typing import Callable

MOD_NOREPEAT = 0x4000
VK = {"F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73, "F5": 0x74,
      "F6": 0x75, "F7": 0x76, "F8": 0x77, "F9": 0x78, "F10": 0x79}


class HotkeyListener:
    def __init__(self) -> None:
        self._bindings: dict[int, Callable[[], None]] = {}
        self._thread: threading.Thread | None = None
        self._running = False
        self._user32 = ctypes.WinDLL("user32", use_last_error=True)

    def bind(self, key: str, cb: Callable[[], None]) -> None:
        vk = VK.get(key.upper())
        if vk:
            self._bindings[vk] = cb

    def _loop(self) -> None:
        for vk in self._bindings:
            self._user32.RegisterHotKey(None, vk, MOD_NOREPEAT, vk)
        msg = wt.MSG()
        while self._running:
            if self._user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
                cb = self._bindings.get(msg.wParam)
                if cb:
                    cb()

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        for vk in self._bindings:
            self._user32.UnregisterHotKey(None, vk)