"""Config loader smoke tests."""
from pathlib import Path

from halo_ce_trainer.config.loader import load_config, TrainerConfig


def test_default_config():
    cfg = load_config("/nonexistent/path.toml")
    assert isinstance(cfg, TrainerConfig)
    assert cfg.process_name == "HaloCampaignEvolved.exe"
    assert cfg.modules["godmode"] is True


def test_toml_override(tmp_path: Path):
    p = tmp_path / "trainer.toml"
    p.write_text(
        'process_name = "halo_test.exe"\n'
        '[modules]\n'
        'godmode = false\n'
        'esp = true\n',
        encoding="utf-8",
    )
    cfg = load_config(str(p))
    assert cfg.process_name == "halo_test.exe"
    assert cfg.modules["godmode"] is False
    assert cfg.modules["esp"] is True