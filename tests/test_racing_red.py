from kano_ring import create_strip
from kano_ring.config import KanoRingConfig
from kano_ring.racing_red import (
    TRAIL_BRIGHTNESS,
    apply_racing_red_frame,
    clear_strip,
    frame_colors,
    trail_indices,
)
from kano_ring.strip import MockColor

RING = KanoRingConfig().led_count  # default ring size (5)


def test_trail_indices_wrap_around_full_ring() -> None:
    assert trail_indices(RING, 0, trail_length=3) == [0, 4, 3]
    assert trail_indices(RING, 1, trail_length=3) == [1, 0, 4]


def test_frame_period_covers_all_ring_leds() -> None:
    """Each offset must be unique so the chase visits every active LED."""
    frames = [tuple(frame_colors(RING, offset)) for offset in range(RING)]
    assert len(set(frames)) == RING

    heads = [frame.index((255, 0, 0)) for frame in frames]
    assert heads == list(range(RING))


def test_frame_colors_use_fading_red_trail() -> None:
    colors = frame_colors(RING, 0)
    assert colors[0] == (TRAIL_BRIGHTNESS[0], 0, 0)
    assert colors[4] == (TRAIL_BRIGHTNESS[1], 0, 0)
    assert colors[3] == (TRAIL_BRIGHTNESS[2], 0, 0)
    assert colors[1] == (0, 0, 0)
    assert all(g == 0 and b == 0 for _, g, b in colors)


def test_apply_racing_red_frame_updates_mock_strip() -> None:
    strip = create_strip()
    strip.begin()

    apply_racing_red_frame(
        strip,
        2,
        make_color=lambda r, g, b: MockColor(r, g, b),
    )

    pixels = strip.pixels()
    assert pixels[2] == MockColor(255, 0, 0)
    assert pixels[1] == MockColor(140, 0, 0)
    assert pixels[0] == MockColor(50, 0, 0)
    assert pixels[3] == MockColor(0, 0, 0)


def test_clear_strip_turns_off_all_pixels() -> None:
    strip = create_strip()
    strip.begin()

    apply_racing_red_frame(
        strip,
        0,
        make_color=lambda r, g, b: MockColor(r, g, b),
    )
    clear_strip(strip, make_color=lambda r, g, b: MockColor(r, g, b))

    assert all(pixel == MockColor(0, 0, 0) for pixel in strip.pixels())
