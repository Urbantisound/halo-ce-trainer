# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.9.x   | ✅        |
| < 0.9   | ❌        |

## Reporting a vulnerability

This project attaches to a running game process and reads/writes its memory.
If you find a security issue (e.g. arbitrary code execution via a malformed
config file, DLL hijack in the overlay, or an unsafe `tasklist` invocation),
please report it privately:

- Open a **private security advisory** on GitHub, or
- Email the maintainers at `security@halo-ce-trainer.invalid`

Please do **not** open a public issue for security reports. We aim to
acknowledge within 72 hours.

## Scope

In scope:
- `halo_ce_trainer/core/process_attach.py`
- `halo_ce_trainer/overlay_core/overlay_host.py`
- `halo_ce_trainer/config/loader.py`

Out of scope:
- Anti-cheat bypass requests
- Multiplayer use cases
- Windows kernel-level issues

## Disclaimer

halo-ce-trainer is provided for **educational and single-player modding
purposes only**. Use at your own risk. The maintainers are not responsible
for bans, data loss, or violations of any terms of service.