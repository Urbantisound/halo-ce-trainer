"""Base Feature interface for trainer modules."""
from __future__ import annotations

from abc import ABC, abstractmethod

from halo_ce_trainer.core.process_attach import ProcessAttach


class Feature(ABC):
    name: str = "base"

    def __init__(self, attach: ProcessAttach) -> None:
        self.attach = attach

    @abstractmethod
    def on_enable(self) -> None: ...

    @abstractmethod
    def on_disable(self) -> None: ...

    def tick(self) -> None:
        """Optional per-frame update hook."""