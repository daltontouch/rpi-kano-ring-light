#!/usr/bin/env python3
"""Fill every LED solid red — quick check that all 10 respond.

Matches KanoHatLeds brightness (150) by default. On a Pi::

    sudo .venv/bin/python3 scripts/fill_all.py
    KANO_RING_BRIGHTNESS=40 sudo -E .venv/bin/python3 scripts/fill_all.py
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

    red = _color(255, 0, 0)
    off = _color(0, 0, 0)
    mode = "mock" if is_mock_mode() else "hardware"

    for index in range(strip.numPixels()):
        strip.setPixelColor(index, red)
    strip.show()
    print(
        f"All {strip.numPixels()} LEDs red "
        f"(pin={cfg.led_pin}, brightness={cfg.led_brightness}, {mode}). "
        "Ctrl+C to clear."
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for index in range(strip.numPixels()):
            strip.setPixelColor(index, off)
        strip.show()
        print("Cleared.")


if __name__ == "__main__":
    main()
