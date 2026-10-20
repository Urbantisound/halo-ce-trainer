"""Helper: dump candidate pattern hits from a running Halo CE build.

Usage: python scripts/dump_offsets.py
"""
from __future__ import annotations

from halo_ce_trainer.core.process_attach import ProcessAttach
from halo_ce_trainer.offsets.patterns import find_all
from halo_ce_trainer.offsets.signatures import (
    GODMODE_SIG, HEALTH_SIG, ENTITY_LIST_SIG,
)


def main() -> None:
    attach = ProcessAttach("HaloCampaignEvolved.exe")
    if not attach.connect():
        print("attach failed")
        return
    base = attach.read_bytes(0x140000000, 0x2000000)
    for name, sig in (("godmode", GODMODE_SIG),
                      ("health", HEALTH_SIG),
                      ("entity_list", ENTITY_LIST_SIG)):
        hits = find_all(base, sig, base_addr=0x140000000)
        print(f"{name}: {len(hits)} hit(s)")
        for h in hits[:5]:
            print(f"  {h:#x}")


if __name__ == "__main__":
    main()