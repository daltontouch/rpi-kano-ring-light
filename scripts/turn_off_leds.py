#!/usr/bin/env python3
"""Turn off all LEDs on the Kano light ring."""

import _bootstrap  # noqa: F401

from kano_ring import create_strip, is_mock_mode
from kano_ring.strip import MockColor


def main() -> None:
    strip = create_strip()
    strip.begin()

    if is_mock_mode():
        off = MockColor(0, 0, 0)
    else:
        from rpi_ws281x import Color  # type: ignore[import-untyped]

        off = Color(0, 0, 0)

    for index in range(strip.numPixels()):
        strip.setPixelColor(index, off)
    strip.show()

    mode = "mock" if is_mock_mode() else "hardware"
    print(f"All {strip.numPixels()} LEDs off ({mode} mode)")


if __name__ == "__main__":
    main()
