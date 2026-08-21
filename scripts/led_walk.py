#!/usr/bin/env python3
"""Light each LED one at a time to find which indices respond.

Useful when only half the ring lights: if indices 0-4 work and 5-9 never
do, the daisy-chain is likely broken after LED 4 (hardware). If the live
set changes with brightness or after disabling audio, it is a signal/power
issue.

Examples (on a Pi)::

    sudo .venv/bin/python3 scripts/led_walk.py
    KANO_RING_BRIGHTNESS=50 sudo -E .venv/bin/python3 scripts/led_walk.py
    KANO_RING_STRIP_TYPE=rgb sudo -E .venv/bin/python3 scripts/led_walk.py
"""

from __future__ import annotations

import _bootstrap  # noqa: F401

import time

from kano_ring import KanoRingConfig, create_strip, is_mock_mode
from kano_ring.strip import MockColor


def _color(r: int, g: int, b: int):
    if is_mock_mode():
        return MockColor(r, g, b)
    from rpi_ws281x import Color  # type: ignore[import-untyped]

    return Color(r, g, b)


def main() -> None:
    cfg = KanoRingConfig.from_env()
    strip = create_strip(cfg)
    strip.begin()

    on = _color(cfg.led_brightness, 0, 0)
    off = _color(0, 0, 0)
    mode = "mock" if is_mock_mode() else "hardware"

    print(
        f"Walking {strip.numPixels()} LEDs "
        f"(pin={cfg.led_pin}, brightness={cfg.led_brightness}, "
        f"dma={cfg.led_dma}, strip_type={cfg.strip_type or 'default'}, {mode})"
    )

    try:
        for index in range(strip.numPixels()):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, on if i == index else off)
            strip.show()
            print(f"  index {index} on — watch which physical LED lit")
            time.sleep(0.6)
    finally:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, off)
        strip.show()
        print("Cleared.")


if __name__ == "__main__":
    main()
