"""Launcher entry point for halo-ce-trainer."""
from __future__ import annotations

import sys

from halo_ce_trainer.bootstrap import TrainerBootstrap
from halo_ce_trainer.ui.control_panel import ControlPanel
from halo_ce_trainer.utils.logging_setup import setup_logging


def main() -> int:
    setup_logging()
    boot = TrainerBootstrap()
    if not boot.start():
        print("[!] Could not attach to Halo: Campaign Evolved. Is it running?")
        return 1

    def _toggle(name: str, enabled: bool) -> None:
        if enabled:
            boot.registry.activate_all(boot.attach, boot.config)
        else:
            boot.registry.deactivate_all()

    panel = ControlPanel(boot.config.modules, _toggle)
    try:
        panel.run()
    finally:
        boot.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())