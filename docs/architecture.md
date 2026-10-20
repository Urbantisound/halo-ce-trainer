# Architecture

```
halo_ce_trainer/
├── bootstrap.py            # entry: attach + registry + overlay
├── config/                 # TOML loader + TrainerConfig dataclass
├── core/
│   ├── process_attach.py   # OpenProcess / ReadProcessMemory / WPM
│   └── module_registry.py  # discovers Feature subclasses
├── features/               # godmode, infinite_ammo, esp, aimbot
├── offsets/                # signatures + pointer chains
├── overlay_core/           # layered topmost window
├── ui/                     # Tkinter control panel
└── utils/                  # logging + Win32 hotkeys
```

## Data flow

1. `run.py` → `TrainerBootstrap.start()`
2. `ProcessAttach` opens a handle to `HaloCampaignEvolved.exe`
3. `ModuleRegistry.discover()` walks `features/` and picks `Feature` subclasses
4. For each module enabled in `trainer.toml`, `on_enable()` is called
5. `OverlayHost` spawns the transparent ESP window on a worker thread
6. Hotkeys (`F8` default) toggle the overlay; the Tk