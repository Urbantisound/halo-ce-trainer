"""ESP overlay: draw entity boxes + names through overlay-core."""
from __future__ import annotations

from halo_ce_trainer.core.process_attach import ProcessAttach
from halo_ce_trainer.features.base import Feature
from halo_ce_trainer.offsets.pointers import resolve_pointer_chain

ENTITY_LIST = (0x02A4F240, 0x10, 0x8)
MAX_ENTITIES = 64


class ESP(Feature):
    name = "esp"

    def __init__(self, attach: ProcessAttach) -> None:
        super().__init__(attach)
        self._list_addr: int | None = None
        self._entities: list[dict] = []

    def on_enable(self) -> None:
        self._list_addr = resolve_pointer_chain(self.attach, ENTITY_LIST)

    def tick(self) -> None:
        if not self._list_addr:
            return
        self._entities.clear()
        raw = self.attach.read_bytes(self._list_addr, MAX_ENTITIES * 8)
        for i in range(MAX_ENTITIES):
            ptr = int.from_bytes(raw[i * 8 : i * 8 + 8], "little")
            if not ptr:
                continue
            data = self.attach.read_bytes(ptr, 0x40)
            self._entities.append({
                "ptr": ptr,
                "pos": (int.from_bytes(data[0x10:0x14], "little"),
                        int.from_bytes(data[0x14:0x18], "little")),
                "team": data[0x28],
            })

    @property
    def entities(self) -> list[dict]:
        return self._entities

    def on_disable(self) -> None:
        self._list_addr = None
        self._entities.clear()