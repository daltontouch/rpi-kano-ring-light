#!/usr/bin/env python3
"""Cycle a simple rainbow pattern across the ring."""

import time

from kano_ring import create_strip, is_mock_mode
from kano_ring.strip import MockColor


def _color(r: int, g: int, b: int):
    if is_mock_mode():
        return MockColor(r, g, b)
    from rpi_ws281x import Color  # type: ignore[import-untyped]

    return Color(r, g, b)


def main() -> None:
    strip = create_strip()
    strip.begin()

    colors = [
        _color(255, 0, 0),
        _color(255, 127, 0),
        _color(255, 255, 0),
        _color(0, 255, 0),
        _color(0, 0, 255),
        _color(75, 0, 130),
        _color(148, 0, 211),
    ]

    for offset in range(strip.numPixels() * 2):
        for index in range(strip.numPixels()):
            strip.setPixelColor(index, colors[(index + offset) % len(colors)])
        strip.show()
        time.sleep(0.15)

    mode = "mock" if is_mock_mode() else "hardware"
    print(f"Rainbow demo complete ({mode} mode)")


if __name__ == "__main__":
    main()
