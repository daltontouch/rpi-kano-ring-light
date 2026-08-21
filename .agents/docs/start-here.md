# Kano Light Ring on Raspberry Pi 3B — Start Here

Research notes for controlling the Kano Computer Kit light ring on a Raspberry Pi 3B running standard Raspberry Pi OS (not Kano OS).

## Hardware Summary

| Setting | Value |
|---------|-------|
| LED type | WS2812 / NeoPixel (addressable RGB) |
| LED count | 10 |
| Data pin | GPIO 18 (BCM) / physical pin 12 |
| Hat button | GPIO 3 (BCM) / physical pin 5 |
| Driver library | `rpi_ws281x` (not `gpiozero`) |
| Typical frequency | 800000 Hz |
| DMA channel | 10 (avoid DMA 5 on Pi 3B) |
| Brightness | 150 (Kano `KanoHatLeds` default; not 255) |
| Run scripts with | `sudo .venv/bin/python3 script.py` (see Quick Start) |

The ring plugs directly onto the GPIO header. Each LED is individually addressable; you cannot control them with simple digital on/off GPIO calls.

## Quick Start

Raspberry Pi OS (Bookworm and later) blocks system-wide `pip install` (PEP 668). Use a virtual environment instead:

```bash
./scripts/install_pi.sh
```

Or manually:

```bash
sudo apt install -y python3-venv python3-full   # if venv is missing
python3 -m venv .venv
.venv/bin/pip install -r requirements-pi.txt
.venv/bin/pip install -e .
```

Run scripts with the venv Python and `sudo` (needed for DMA/PWM access):

```bash
source .venv/bin/activate
sudo python3 scripts/turn_off_leds.py
```

Or without activating the venv:

```bash
sudo .venv/bin/python3 scripts/turn_off_leds.py
sudo ./scripts/run_pi.sh scripts/rainbow_demo.py
```

Plain `python3 scripts/...` uses system Python and will not see packages installed in `.venv`.

If you must install into system Python anyway (not recommended), add `--break-system-packages` to pip.

Minimal test script:

```python
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 10
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 150  # KanoHatLeds default
LED_INVERT = False
LED_CHANNEL = 0

strip = PixelStrip(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
    LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
)
strip.begin()

strip.setPixelColor(0, Color(255, 0, 0))  # first LED red
strip.show()
```

Run with:

```bash
sudo .venv/bin/python3 your_script.py
```

## Public GitHub Examples

### 1. [KanoComputing/kano-peripherals](https://github.com/KanoComputing/kano-peripherals) — Official Kano source

Best reference for how Kano OS drives the ring.

| File | Purpose |
|------|---------|
| [`kano_hat_leds.py`](https://github.com/KanoComputing/kano-peripherals/blob/master/libs/pi_hat/library/python/kano_pi_hat/kano_hat_leds.py) | `KanoHatLeds` class — 10 LEDs, pin 18, DMA 10 |
| [`leds.py`](https://github.com/KanoComputing/kano-peripherals/blob/master/libs/pi_hat/examples/python/ck2_lite/leds.py) | Minimal example setting individual LEDs |
| [`turn-off-hat-leds`](https://github.com/KanoComputing/kano-peripherals/blob/master/bin/turn-off-hat-leds) | Utility to clear the ring |

Uses Kano's `neopixel` wrapper around `rpi_ws281x`. Requires the full Kano peripherals package to run as-is.

### 2. [Aml0n/kano_light_ring_clock](https://github.com/Aml0n/kano_light_ring_clock) — Community clock project

Full project for the Kano ring on plain Raspberry Pi OS.

| File | Purpose |
|------|---------|
| [`kano_light_ring.py`](https://github.com/Aml0n/kano_light_ring_clock/blob/master/kano_light_ring.py) | Clock with hour/minute/sunrise animations |
| [`testPrograms/`](https://github.com/Aml0n/kano_light_ring_clock/tree/master/testPrograms) | Color tests and animation experiments |

Uses `rpi_ws281x` directly with documented Kano ring settings. Includes a pygame "pi-less" mode for development off the Pi.

### 3. [mike1000000000/kano_led_ring](https://github.com/mike1000000000/kano_led_ring) — Minimal starter

Smallest working example — turn all ring LEDs off.

| File | Purpose |
|------|---------|
| [`turn_off_leds.py`](https://github.com/mike1000000000/kano_led_ring/blob/master/turn_off_leds.py) | ~15 lines using `PixelStrip` on GPIO 18 |

Good starting point for verifying hardware and library setup.

### 4. [marcelfarres/pimonitor](https://github.com/marcelfarres/pimonitor) — Reusable abstraction

Clean wrapper inspired by Kano's original code, designed for standard Raspberry Pi OS.

| File | Purpose |
|------|---------|
| [`pimonitor/kano_hat.py`](https://github.com/marcelfarres/pimonitor/blob/master/pimonitor/kano_hat.py) | `KanoHat` class for the 10-LED ring and hat button |

Documents pin mappings from Kano's `kano-peripherals` C/Python code. Good if you want a small library rather than inline `rpi_ws281x` calls.

### 5. [scollovati/kano_make_light_lightboard_animations](https://github.com/scollovati/kano_make_light_lightboard_animations) — Related, different hardware

Animations for the **Kano Make Light lightboard** (LED grid), not the Computer Kit ring.

Uses Kano's `make_light` Python API. Useful only if you also have a lightboard — not the right API for the 10-LED ring.

## Underlying Libraries

| Repo | Role |
|------|------|
| [jgarff/rpi_ws281x](https://github.com/jgarff/rpi_ws281x) | C library for WS281x LEDs on Raspberry Pi |
| [rpi-ws281x/rpi-ws281x-python](https://github.com/rpi-ws281x/rpi-ws281x-python) | Python bindings (`pip install rpi-ws281x`) |

## Common Pitfalls

1. **Do not use `gpiozero` or direct GPIO writes** — the ring needs WS2812 timing via PWM/DMA.
2. **Run with `sudo`** — `rpi_ws281x` needs root for DMA/PWM access.
3. **Use DMA 10, not 5** — DMA channel 5 can conflict on Pi 3B.
4. **Pin 18, not 21** — community reports vary, but Kano's official code and working community examples consistently use GPIO 18.
5. **Color order** — WS2812 LEDs use GRB order by default; if colors look wrong, try `KANO_RING_STRIP_TYPE=rgb`.
6. **Disable onboard audio** — GPIO 18 PWM conflicts with the Pi audio driver. If only the first few LEDs light, or the ring flickers, add `dtparam=audio=off` to `/boot/firmware/config.txt` (or `/boot/config.txt` on older images), reboot, and retest. Kano OS often avoided this clash.
7. **Brightness** — Kano's `KanoHatLeds` defaults to **150**, not 255. Full brightness on the Pi's 5V rail can brown out later LEDs in the chain so only ~half the ring lights.

## Only half the ring lights?

Kano's driver is a single strip of 10 on GPIO 18 (`Adafruit_NeoPixel(10, 18, dma=10)`). There is no second data pin for the other five LEDs. If five never light:

1. Run `sudo .venv/bin/python3 scripts/led_walk.py` and note which **indices** light.
2. Retry at low brightness: `KANO_RING_BRIGHTNESS=40 sudo -E .venv/bin/python3 scripts/fill_all.py`
3. Disable audio (pitfall 6) and reboot.
4. If indices 0–4 always work and 5–9 never do (at any brightness), the daisy-chain between those LEDs is likely broken — software cannot fix that.

## Recommended Path

1. Start with **mike1000000000/kano_led_ring** to verify hardware and library setup.
2. Reference **KanoComputing/kano-peripherals** for authoritative pin and config details.
3. Use **Aml0n/kano_light_ring_clock** or **marcelfarres/pimonitor** as templates for a full project.

## Community Discussion

- [Raspberry Pi Forums — Kano Light Circle](https://forums.raspberrypi.com/viewtopic.php?t=328273)
- [Raspberry Pi Forums — Inherited Kano kit LED ring](https://forums.raspberrypi.com/viewtopic.php?t=399085)
