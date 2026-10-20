"""Godmode patch: NOP the damage-apply branch in the player health routine."""
from __future__ import annotations

from halo_ce_trainer.core.process_attach import ProcessAttach
from halo_ce_trainer.features.base import Feature
from halo_ce_trainer.offsets.patterns import find_pattern
from halo_ce_trainer.offsets.signatures import GODMODE_SIG


class Godmode(Feature):
    name = "godmode"

    def __init__(self, attach: ProcessAttach) -> None:
        super().__init__(attach)
        self._addr: int | None = None
        self._orig: bytes | None = None

    def on_enable(self) -> None:
        base = self.attach.read_bytes(0x140000000, 0x2000000)
        self._addr = find_pattern(base, GODMODE_SIG, base_addr=0x140000000)
        if not self._addr:
            raise RuntimeError("godmode signature not found")
        self._orig = self.attach.read_bytes(self._addr, 6)
        self.attach.write_bytes(self._addr, b"\x90" * 6)

    def on_disable(self) -> None:
        if self._addr and self._orig:
            self.attach.write_bytes(self._addr, self._orig)
            self._addr, self._orig = None, None