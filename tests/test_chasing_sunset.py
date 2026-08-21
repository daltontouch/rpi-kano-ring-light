from kano_ring import create_strip
from kano_ring.chasing_sunset import (
    DEFAULT_TRAIL_LENGTH,
    apply_chasing_sunset_frame,
    clear_strip,
    frame_colors,
    sunset_color,
    trail_indices,
)
from kano_ring.strip import MockColor


def test_trail_indices_wrap_around_full_ring() -> None:
    assert trail_indices(10, 0, trail_length=5) == [0, 9, 8, 7, 6]
    assert trail_indices(10, 1, trail_length=5) == [1, 0, 9, 8, 7]


def test_sunset_color_interpolates_red_to_yellow() -> None:
    assert sunset_color(0, 5) == (255, 0, 0)
    assert sunset_color(4, 5) == (255, 255, 0)
    assert sunset_color(2, 5) == (255, 128, 0)


def test_frame_period_covers_all_ten_leds() -> None:
    """Each offset must be unique so the chase visits the whole ring."""
    frames = [tuple(frame_colors(10, offset)) for offset in range(10)]
    assert len(set(frames)) == 10

    heads = [frame.index((255, 0, 0)) for frame in frames]
    assert heads == list(range(10))


def test_frame_colors_use_yellow_to_red_trail() -> None:
    colors = frame_colors(10, 0, trail_length=DEFAULT_TRAIL_LENGTH)
    assert colors[0] == (255, 0, 0)
    assert colors[9] == (255, 64, 0)
    assert colors[8] == (255, 128, 0)
    assert colors[7] == (255, 191, 0)
    assert colors[6] == (255, 255, 0)
    assert colors[1] == (0, 0, 0)


def test_apply_chasing_sunset_frame_updates_mock_strip() -> None:
    strip = create_strip()
    strip.begin()

    apply_chasing_sunset_frame(
        strip,
        2,
        make_color=lambda r, g, b: MockColor(r, g, b),
    )

    pixels = strip.pixels()
    assert pixels[2] == MockColor(255, 0, 0)
    assert pixels[1] == MockColor(255, 64, 0)
    assert pixels[0] == MockColor(255, 128, 0)
    assert pixels[9] == MockColor(255, 191, 0)
    assert pixels[8] == MockColor(255, 255, 0)
    assert pixels[3] == MockColor(0, 0, 0)


def test_clear_strip_turns_off_all_pixels() -> None:
    strip = create_strip()
    strip.begin()

    apply_chasing_sunset_frame(
        strip,
        0,
        make_color=lambda r, g, b: MockColor(r, g, b),
    )
    clear_strip(strip, make_color=lambda r, g, b: MockColor(r, g, b))

    assert all(pixel == MockColor(0, 0, 0) for pixel in strip.pixels())
