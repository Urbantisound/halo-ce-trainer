"""Attach to the Halo: Campaign Evolved process and expose r/w handles."""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import logging

log = logging.getLogger("halo.trainer.attach")

PROCESS_ALL_ACCESS = 0x1F0FFF
SE_DEBUG_NAME = "SeDebugPrivilege"


class ProcessAttach:
    def __init__(self, process_name: str) -> None:
        self.process_name = process_name
        self.pid: int | None = None
        self.handle: int | None = None
        self._k32 = ctypes.WinDLL("kernel32", use_last_error=True)

    def _find_pid(self) -> int | None:
        import subprocess
        try:
            out = subprocess.check_output(
                ["tasklist", "/FI", f"IMAGENAME eq {self.process_name}", "/FO", "CSV", "/NH"],
                text=True, stderr=subprocess.DEVNULL,
            )
        except Exception:
            return None
        for line in out.splitlines():
            parts = [p.strip('"') for p in line.split('","')]
            if len(parts) >= 2 and parts[0].lower() == self.process_name.lower():
                try:
                    return int(parts[1])
                except ValueError:
                    continue
        return None

    def connect(self) -> bool:
        pid = self._find_pid()
        if not pid:
            return False
        h = self._k32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if not h:
            log.error("OpenProcess failed: %s", ctypes.get_last_error())
            return False
        self.pid, self.handle = pid, h
        return True

    def enable_debug_privilege(self) -> bool:
        advapi = ctypes.WinDLL("advapi32", use_last_error=True)
        token = wt.HANDLE()
        if not advapi.OpenProcessToken(self._k32.GetCurrentProcess(), 0x28, ctypes.byref(token)):
            return False
        luid = ctypes.c_uint64()
        if not advapi.LookupPrivilegeValueW(None, SE_DEBUG_NAME, ctypes.byref(luid)):
            return False
        tp = (ctypes.c_uint64 * 2)(luid.value, 0x2)
        class _TP(ctypes.Structure):
            _fields_ = [("Count", wt.DWORD), ("Priv", ctypes.POINTER(ctypes.c_uint64))]
        tpv = _TP(1, ctypes.cast(tp, ctypes.POINTER(ctypes.c_uint64)))
        return bool(advapi.AdjustTokenPrivileges(token, False, ctypes.byref(tpv), 0, None, None))

    def read_bytes(self, address: int, size: int) -> bytes:
        buf = ctypes.create_string_buffer(size)
        read = ctypes.c_size_t(0)
        self._k32.ReadProcessMemory(self.handle, ctypes.c_void_p(address),
                                    buf, size, ctypes.byref(read))
        return buf.raw[: read.value]

    def write_bytes(self, address: int, data: bytes) -> bool:
        written = ctypes.c_size_t(0)
        return bool(self._k32.WriteProcessMemory(
            self.handle, ctypes.c_void_p(address), data, len(data), ctypes.byref(written)
        )) and written.value == len(data)

    def detach(self) -> None:
        if self.handle:
            self._k32.CloseHandle(self.handle)
        self.handle, self.pid = None, None