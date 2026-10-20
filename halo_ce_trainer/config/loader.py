"""Config loader for trainer runtime settings (TOML + env overrides)."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore


@dataclass
class OverlayConfig:
    enabled: bool = True
    opacity: float = 0.82
    hotkey_toggle: str = "F8"
    font: str = "Consolas"


@dataclass
class TrainerConfig:
    process_name: str = "HaloCampaignEvolved.exe"
    game_build: str = "2026.1"
    overlay: OverlayConfig = field(default_factory=OverlayConfig)
    modules: Dict[str, bool] = field(default_factory=lambda: {
        "godmode": True,
        "infinite_ammo": True,
        "esp": False,
        "aimbot": False,
    })
    log_level: str = "INFO"


def _deep_merge(base: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: str | None = None) -> TrainerConfig:
    cfg = TrainerConfig()
    candidates = [Path(path)] if path else [
        Path.cwd() / "trainer.toml",
        Path.home() / ".halo-ce-trainer" / "trainer.toml",
    ]
    for p in candidates:
        if p and p.is_file():
            data = tomllib.loads(p.read_text(encoding="utf-8"))
            merged = _deep_merge(cfg.__dict__, data)
            cfg = TrainerConfig(**merged)
            break
    if os.getenv("HALO_TRAINER_LOG"):
        cfg.log_level = os.environ["HALO_TRAINER_LOG"]
    return cfg