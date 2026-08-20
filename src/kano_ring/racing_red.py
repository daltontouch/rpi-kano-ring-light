from __future__ import annotations

import time
from typing import Callable

from kano_ring.strip import MockColor, is_mock_mode

RED = (255, 0, 0)
OFF = (0, 0, 0)


def lit_indices(num_pixels: int, offset: int, light_count: int = 2) -> list[int]:
    """Return LED indices lit for one frame of the racing red animation."""
    if num_pixels <= 0 or light_count <= 0:
        return []

    spacing = max(1, num_pixels // light_count)
    return [(offset + index * spacing) % num_pixels for index in range(light_count)]


def frame_colors(
    num_pixels: int,
    offset: int,
    light_count: int = 2,
) -> list[tuple[int, int, int]]:
    """Return RGB tuples for each pixel in one animation frame."""
    pixels = [OFF] * num_pixels
    for index in lit_indices(num_pixels, offset, light_count):
        pixels[index] = RED
    return pixels


def _make_color(r: int, g: int, b: int):
    if is_mock_mode():
        return MockColor(r, g, b)
    from rpi_ws281x import Color  # type: ignore[import-untyped]

    return Color(r, g, b)


def apply_racing_red_frame(
    strip,
    offset: int,
    *,
    light_count: int = 2,
    make_color: Callable[[int, int, int], object] | None = None,
) -> None:
    """Paint one frame of the racing red animation onto the strip."""
    color_fn = make_color or _make_color
    colors = frame_colors(strip.numPixels(), offset, light_count)
    for index, rgb in enumerate(colors):
        strip.setPixelColor(index, color_fn(*rgb))


def clear_strip(strip, make_color: Callable[[int, int, int], object] | None = None) -> None:
    """Turn off every LED on the strip."""
    color_fn = make_color or _make_color
    off = color_fn(*OFF)
    for index in range(strip.numPixels()):
        strip.setPixelColor(index, off)
    strip.show()


def run_racing_red(
    strip,
    *,
    light_count: int = 2,
    delay: float = 0.1,
) -> None:
    """Race red lights around the ring until interrupted with Ctrl+C."""
    strip.begin()
    offset = 0

    try:
        while True:
            apply_racing_red_frame(strip, offset, light_count=light_count)
            strip.show()
            time.sleep(delay)
            offset = (offset + 1) % strip.numPixels()
    except KeyboardInterrupt:
        clear_strip(strip)
