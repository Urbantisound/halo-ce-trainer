# Contributing to halo-ce-trainer

Thanks for your interest in the Halo: Campaign Evolved Trainer project.

## How to contribute

1. Fork the repo and create a feature branch off `main`.
2. Keep new features under `halo_ce_trainer/features/` and inherit from
   `halo_ce_trainer.features.base.Feature`.
3. Add or update signatures in `halo_ce_trainer/offsets/signatures.py` when
   the game build changes — do not hardcode absolute addresses.
4. Add unit tests under `tests/` where feasible (pattern scanning, config
   loading, pointer-chain resolution are all testable without the game).
5. Run `pytest -q` before opening a PR.

## Code style

- Python 3.11+, type hints required on public functions.
- `ruff` + `black` are recommended.
- No wildcard imports.

## Reporting offsets for new game builds

Open an issue titled `offsets: build XXXX` and include the byte signatures
you found via Cheat Engine / IDA. Pull requests that update `signatures.py`
and `pointers.py` are very welcome.

## Legal

This is a single-player modding / research project. Do not use it in
multiplayer — you will be banned, and it's not what this repo is for.