"""Infinite ammo: freeze the magazine counter each tick."""
from __future__ import annotations

from halo_ce_trainer.core.process_attach import ProcessAttach
from halo_ce_trainer.features.base import Feature
from halo_ce_trainer.offsets.pointers import resolve_pointer_chain


class InfiniteAmmo(Feature):
    name = "infinite_ammo"
    POINTER_CHAIN = (0x02A4F1C0, 0x18, 0x2C, 0x0)

    def __init__(self, attach: ProcessAttach) -> None:
        super().__init__(attach)
        self._magazine_addr: int | None = None

    def on_enable(self) -> None:
        self._magazine_addr = resolve_pointer_chain(self.attach, self.POINTER_CHAIN)

    def tick(self) -> None:
        if self._magazine_addr:
            self.attach.write_bytes(self._magazine_addr, (60).to_bytes(4, "little"))

    def on_disable(self) -> None:
        self._magazine_addr = None