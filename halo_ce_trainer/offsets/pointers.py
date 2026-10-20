"""Resolve multi-level pointer chains in the target process."""
from __future__ import annotations

from halo_ce_trainer.core.process_attach import ProcessAttach


def resolve_pointer_chain(attach: ProcessAttach, chain: tuple[int, ...]) -> int | None:
    base = chain[0]
    for offset in chain[1:-1]:
        raw = attach.read_bytes(base, 8)
        if len(raw) != 8:
            return None
        base = int.from_bytes(raw, "little") + offset
    return base + chain[-1]