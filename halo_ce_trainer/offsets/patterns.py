"""Wildcard-aware byte pattern scanner (AOB style)."""
from __future__ import annotations

from typing import Optional


def find_pattern(buffer: bytes, pattern: bytes, base_addr: int = 0) -> Optional[int]:
    """Return absolute address of first match, or None."""
    if not pattern or len(pattern) > len(buffer):
        return None
    idx = buffer.find(pattern)
    return base_addr + idx if idx >= 0 else None


def find_all(buffer: bytes, pattern: bytes, base_addr: int = 0) -> list[int]:
    out: list[int] = []
    start = 0
    while True:
        idx = buffer.find(pattern, start)
        if idx < 0:
            break
        out.append(base_addr + idx)
        start = idx + 1
    return out