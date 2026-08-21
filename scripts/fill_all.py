#!/usr/bin/env python3
"""Fill the ring with a diagnostic two-tone pattern.

Lights the configured ring (default 5 LEDs) in a two-tone split for
diagnostics. Matches KanoHatLeds brightness (150) by default.

On a Pi::

    sudo .venv/bin/python3 scripts/fill_all.py
    KANO_RING_BRIGHTNESS=40 sudo -E .venv/bin/python3 scripts/fill_all.py

For pin / dual-chain checks, use scripts/probe_half_ring.py.
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

    n = strip.numPixels()
    red = _color(255, 0, 0)
    blue = _color(0, 0, 255)
    off = _color(0, 0, 0)
    mode = "mock" if is_mock_mode() else "hardware"

    split = n // 2
    for index in range(n):
        strip.setPixelColor(index, red if index < split else blue)
    strip.show()

    print(
        f"Set {n} pixels (pin={cfg.led_pin}, brightness={cfg.led_brightness}, {mode}).\n"
        f"  indices 0-{split - 1} = RED, {split}-{n - 1} = BLUE.\n"
        "Ctrl+C to clear."
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for index in range(n):
            strip.setPixelColor(index, off)
        strip.show()
        print("Cleared.")


if __name__ == "__main__":
    main()
