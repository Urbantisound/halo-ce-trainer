"""Transparent always-on-top overlay window for ESP / HUD."""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import threading

WS_EX_LAYERED = 0x80000
WS_EX_TRANSPARENT = 0x20
WS_EX_TOPMOST = 0x8


class OverlayHost:
    def __init__(self, cfg) -> None:
        self.cfg = cfg
        self._thread: threading.Thread | None = None
        self._running = False
        self._user32 = ctypes.WinDLL("user32", use_last_error=True)

    def _create_window(self) -> int:
        hwnd = self._user32.CreateWindowExW(
            WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST,
            "STATIC", "halo-ce-trainer overlay",
            0x80000000, 0, 0, 1920, 1080, None, None, None, None,
        )
        return hwnd or 0

    def _loop(self) -> None:
        hwnd = self._create_window()
        if not hwnd:
            return
        self._user32.ShowWindow(hwnd, 5)
        while self._running:
            self._user32.MsgWaitForMultipleObjectsEx(
                0, None, 16, 0x04FF, 0x0004
            )

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def close(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)