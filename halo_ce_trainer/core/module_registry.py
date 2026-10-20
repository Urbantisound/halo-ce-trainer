"""Discover and activate feature modules under `features/`."""
from __future__ import annotations

import importlib
import inspect
import logging
import pkgutil
from typing import Dict, List

from halo_ce_trainer.core.process_attach import ProcessAttach
from halo_ce_trainer.features.base import Feature

log = logging.getLogger("halo.trainer.registry")


class ModuleRegistry:
    def __init__(self) -> None:
        self._classes: List[type[Feature]] = []
        self.active: Dict[str, Feature] = {}

    def discover(self) -> None:
        import halo_ce_trainer.features as pkg
        for modinfo in pkgutil.iter_modules(pkg.__path__):
            if modinfo.name.startswith("_") or modinfo.name == "base":
                continue
            mod = importlib.import_module(f"halo_ce_trainer.features.{modinfo.name}")
            for _, obj in inspect.getmembers(mod, inspect.isclass):
                if issubclass(obj, Feature) and obj is not Feature:
                    self._classes.append(obj)

    def activate_all(self, attach: ProcessAttach, config) -> None:
        for cls in self._classes:
            name = cls.name
            if not config.modules.get(name, False):
                continue
            inst = cls(attach)
            try:
                inst.on_enable()
                self.active[name] = inst
            except Exception as exc:  # noqa: BLE001
                log.warning("module %s failed: %s", name, exc)

    def deactivate_all(self) -> None:
        for inst in self.active.values():
            try:
                inst.on_disable()
            except Exception:  # noqa: BLE001
                pass
        self.active.clear()