"""Entry bootstrap: wires process attach, module registry, and overlay."""
from __future__ import annotations

import logging
from typing import Optional

from halo_ce_trainer.core.process_attach import ProcessAttach
from halo_ce_trainer.core.module_registry import ModuleRegistry
from halo_ce_trainer.config.loader import load_config
from halo_ce_trainer.overlay_core.overlay_host import OverlayHost

log = logging.getLogger("halo.trainer.bootstrap")


class TrainerBootstrap:
    def __init__(self, config_path: Optional[str] = None) -> None:
        self.config = load_config(config_path)
        self.attach = ProcessAttach(self.config.process_name)
        self.registry = ModuleRegistry()
        self.overlay: Optional[OverlayHost] = None

    def start(self) -> bool:
        if not self.attach.connect():
            log.error("could not attach to %s", self.config.process_name)
            return False
        self.attach.enable_debug_privilege()
        self.overlay = OverlayHost(self.config.overlay)
        self.registry.discover()
        self.registry.activate_all(self.attach, self.config)
        log.info("trainer online: %d modules", len(self.registry.active))
        return True

    def shutdown(self) -> None:
        self.registry.deactivate_all()
        if self.overlay:
            self.overlay.close()
        self.attach.detach()