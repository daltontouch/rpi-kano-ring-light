from __future__ import annotations

import time
from typing import Callable

from kano_ring.strip import MockColor, is_mock_mode

OFF = (0, 0, 0)

# Warm sunset endpoints: red at the leading edge, yellow at the trailing edge.
SUNSET_RED = (255, 0, 0)
SUNSET_YELLOW = (255, 255, 0)

# Longer trail than racing red so the yellow-to-red blend reads smoothly.
DEFAULT_TRAIL_LENGTH = 5


def trail_indices(num_pixels: int, offset: int, trail_length: int) -> list[int]:
    """Return LED indices for the chase (head at offset, then behind clockwise)."""
    if num_pixels <= 0 or trail_length <= 0:
        return []

    length = min(trail_length, num_pixels)
    return [(offset - step) % num_pixels for step in range(length)]


def sunset_color(step: int, trail_length: int) -> tuple[int, int, int]:
    """Interpolate from red (head) to yellow (tail) along the chase."""
    if trail_length <= 1:
        return SUNSET_RED

    # step 0 is the head; higher steps sit further behind on the ring.
    t = step / (trail_length - 1)
    red = SUNSET_RED[0]
    green = round(SUNSET_YELLOW[1] * t)
    return (red, green, 0)


def frame_colors(
    num_pixels: int,
    offset: int,
    *,
    trail_length: int = DEFAULT_TRAIL_LENGTH,
) -> list[tuple[int, int, int]]:
    """Return RGB tuples for each pixel in one chasing-sunset frame."""
    pixels = [OFF] * num_pixels
    indices = trail_indices(num_pixels, offset, trail_length)
    for step, index in enumerate(indices):
        pixels[index] = sunset_color(step, len(indices))
    return pixels


def _make_color(r: int, g: int, b: int):
    if is_mock_mode():
        return MockColor(r, g, b)
    from rpi_ws281x import Color  # type: ignore[import-untyped]

    return Color(r, g, b)


def apply_chasing_sunset_frame(
    strip,
    offset: int,
    *,
    trail_length: int = DEFAULT_TRAIL_LENGTH,
    make_color: Callable[[int, int, int], object] | None = None,
) -> None:
    """Paint one frame of the chasing sunset animation onto the strip."""
    color_fn = make_color or _make_color
    colors = frame_colors(strip.numPixels(), offset, trail_length=trail_length)
    for index, rgb in enumerate(colors):
        strip.setPixelColor(index, color_fn(*rgb))


def clear_strip(strip, make_color: Callable[[int, int, int], object] | None = None) -> None:
    """Turn off every LED on the strip."""
    color_fn = make_color or _make_color
    off = color_fn(*OFF)
    for index in range(strip.numPixels()):
        strip.setPixelColor(index, off)
    strip.show()


def run_chasing_sunset(
    strip,
    *,
    delay: float = 0.08,
    trail_length: int = DEFAULT_TRAIL_LENGTH,
) -> None:
    """Chase a yellow-to-red sunset gradient clockwise until Ctrl+C."""
    strip.begin()
    offset = 0
    num_pixels = strip.numPixels()

    try:
        while True:
            apply_chasing_sunset_frame(strip, offset, trail_length=trail_length)
            strip.show()
            time.sleep(delay)
            offset = (offset + 1) % num_pixels
    except KeyboardInterrupt:
        clear_strip(strip)
