"""Configure file + console logging for the trainer."""
from __future__ import annotations

import logging
from pathlib import Path


def setup_logging(level: str = "INFO", log_dir: str | None = None) -> None:
    path = Path(log_dir or (Path.home() / ".halo-ce-trainer" / "logs"))
    path.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(path / "trainer.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )