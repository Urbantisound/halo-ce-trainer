"""Unit tests for the AOB pattern scanner."""
from halo_ce_trainer.offsets.patterns import find_pattern, find_all


def test_find_simple():
    buf = b"\x00\x00\x48\x89\x5C\x24\x08\x00"
    assert find_pattern(buf, b"\x48\x89\x5C\x24\x08") == 2


def test_find_with_base():
    buf = b"\xAA\xBB\xCC\xDD"
    assert find_pattern(buf, b"\xCC\xDD", base_addr=0x1000) == 0x1002


def test_find_all():
    buf = b"\x90\x90\x90\x90\x90"
    assert find_all(buf, b"\x90") == [0, 1, 2, 3, 4]


def test_missing():
    assert find_pattern(b"\x00" * 16, b"\xFF\xFF") is None