from __future__ import annotations

import signal
import time
from typing import Callable

from kano_ring.strip import MockColor, is_mock_mode

OFF = (0, 0, 0)

# Brightness levels for the racing trail (head first, then fading tail).
# An asymmetric trail makes a full-ring rotation visible; two identical
# opposite lights would look stuck on half the circle.
TRAIL_BRIGHTNESS = (255, 140, 50)


def trail_indices(num_pixels: int, offset: int, trail_length: int) -> list[int]:
    """Return LED indices for the racing trail (head at offset, then behind)."""
    if num_pixels <= 0 or trail_length <= 0:
        return []

    length = min(trail_length, num_pixels)
    return [(offset - step) % num_pixels for step in range(length)]


def frame_colors(
    num_pixels: int,
    offset: int,
    *,
    trail: tuple[int, ...] = TRAIL_BRIGHTNESS,
) -> list[tuple[int, int, int]]:
    """Return RGB tuples for each pixel in one full-ring racing frame."""
    pixels = [OFF] * num_pixels
    for step, index in enumerate(trail_indices(num_pixels, offset, len(trail))):
        level = trail[step]
        pixels[index] = (level, 0, 0)
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
    trail: tuple[int, ...] = TRAIL_BRIGHTNESS,
    make_color: Callable[[int, int, int], object] | None = None,
) -> None:
    """Paint one frame of the racing red animation onto the strip."""
    color_fn = make_color or _make_color
    colors = frame_colors(strip.numPixels(), offset, trail=trail)
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
    delay: float = 0.08,
    trail: tuple[int, ...] = TRAIL_BRIGHTNESS,
) -> None:
    """Race a red trail around the full ring until interrupted (Ctrl+C or SIGTERM)."""
    strip.begin()
    offset = 0
    num_pixels = strip.numPixels()
    stop_requested = False

    def _request_stop(signum: int, frame) -> None:
        del signum, frame
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGTERM, _request_stop)
    signal.signal(signal.SIGINT, _request_stop)

    try:
        while not stop_requested:
            apply_racing_red_frame(strip, offset, trail=trail)
            strip.show()
            time.sleep(delay)
            offset = (offset + 1) % num_pixels
    finally:
        clear_strip(strip)
