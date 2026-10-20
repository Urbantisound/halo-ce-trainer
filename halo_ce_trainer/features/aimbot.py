"""Aimbot: snap view angles toward nearest enemy in FOV cone."""
from __future__ import annotations

import math

from halo_ce_trainer.core.process_attach import ProcessAttach
from halo_ce_trainer.features.base import Feature
from halo_ce_trainer.offsets.pointers import resolve_pointer_chain

VIEW_ANGLES = (0x02A4F300, 0x8, 0x0)
CAMERA_POS = (0x02A4F300, 0x8, 0x14)


class Aimbot(Feature):
    name = "aimbot"
    FOV_DEG = 12.0
    SMOOTH = 0.35

    def __init__(self, attach: ProcessAttach) -> None:
        super().__init__(attach)
        self._angles_addr: int | None = None
        self._cam_addr: int | None = None

    def on_enable(self) -> None:
        self._angles_addr = resolve_pointer_chain(self.attach, VIEW_ANGLES)
        self._cam_addr = resolve_pointer_chain(self.attach, CAMERA_POS)

    def tick(self) -> None:
        if not self._angles_addr or not self._cam_addr:
            return
        me = self.attach.read_bytes(self._cam_addr, 12)
        mx = int.from_bytes(me[0:4], "little", signed=True)
        mz = int.from_bytes(me[8:12], "little", signed=True)
        best, best_d = None, self.FOV_DEG
        for ent in getattr(self, "_entities", []):
            ex, ez = ent["pos"]
            dx, dz = ex - mx, ez - mz
            yaw = math.degrees(math.atan2(dz, dx))
            d = abs(yaw)
            if d < best_d:
                best, best_d = yaw, d
        if best is not None:
            cur = self.attach.read_bytes(self._angles_addr, 4)
            cur_yaw = int.from_bytes(cur, "little", signed=True) / 1000.0
            new_yaw = cur_yaw + (best - cur_yaw) * self.SMOOTH
            self.attach.write_bytes(self._angles_addr, int(new_yaw * 1000).to_bytes(4, "little", signed=True))

    def on_disable(self) -> None:
        self._angles_addr = None
        self._cam_addr = None