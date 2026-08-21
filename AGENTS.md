# Agent Instructions

This repository controls the Kano Computer Kit light ring (5 active WS2812 NeoPixels on GPIO 18 by default; physical ring has 10) on a Raspberry Pi 3B.

## Cursor Cloud specific instructions

Cloud agents run on Ubuntu x86 VMs, not on Raspberry Pi hardware. Follow these rules when working in the cloud:

- **Use mock mode for development and tests.** The `kano_ring` package auto-detects when `rpi_ws281x` is unavailable and falls back to an in-memory mock strip. Do not try to install or import `rpi-ws281x` in the cloud environment.
- **Run tests with:** `python3 -m pytest -q`
- **Run demo scripts with:** `python3 scripts/<script>.py` (no `sudo` needed in mock mode)
- **Hardware-only work** (DMA, PWM, real LED output) must be documented in PR descriptions and verified on a physical Pi. See `.agents/docs/start-here.md` for pin mappings and pitfalls.
- **On a real Pi**, run `./scripts/install_pi.sh`, then use the venv: `source .venv/bin/activate && sudo python3 scripts/<script>.py` (or `sudo .venv/bin/python3 scripts/<script>.py`). Do not use bare system `python3` — it cannot see packages in `.venv`.

### Project layout

| Path | Purpose |
|------|---------|
| `src/kano_ring/` | Shared library — config constants and hardware/mock strip |
| `scripts/` | Runnable examples |
| `tests/` | Unit tests (mock mode, no hardware) |
| `.agents/docs/start-here.md` | Hardware research and community references |
| `requirements.txt` | Cloud/dev dependencies |
| `requirements-pi.txt` | Pi-only hardware dependencies |

### Common tasks

- Adding a new animation: implement in `src/kano_ring/`, add a script under `scripts/`, add tests under `tests/`.
- Changing LED config (count, pin, DMA): edit `src/kano_ring/config.py` only — do not scatter magic numbers.
