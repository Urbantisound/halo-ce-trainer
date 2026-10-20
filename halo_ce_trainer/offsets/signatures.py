"""Byte signatures for pattern scanning (2026.1 game build)."""

# NOP target inside player damage routine
GODMODE_SIG = b"\x48\x89\x5C\x24\x08\x48\x89\x74\x24\x10\x57\x48\x83\xEC\x20"

# Player health struct write site
HEALTH_SIG = b"\x89\x81\xA0\x00\x00\x00\x48\x8B\x5C\x24"

# Entity list accessor prologue
ENTITY_LIST_SIG = b"\x48\x8B\x05\x00\x00\x00\x00\x48\x85\xC0\x74\x10"