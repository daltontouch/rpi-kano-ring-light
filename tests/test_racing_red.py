from kano_ring import create_strip
from kano_ring.racing_red import (
    apply_racing_red_frame,
    clear_strip,
    frame_colors,
    lit_indices,
)
from kano_ring.strip import MockColor


def test_lit_indices_two_red_lights_on_ten_led_ring() -> None:
    assert lit_indices(10, 0, light_count=2) == [0, 5]
    assert lit_indices(10, 1, light_count=2) == [1, 6]


def test_frame_colors_only_red_pixels_are_lit() -> None:
    colors = frame_colors(10, 3, light_count=2)
    assert colors.count((255, 0, 0)) == 2
    assert colors[3] == (255, 0, 0)
    assert colors[8] == (255, 0, 0)
    assert all(color in {(255, 0, 0), (0, 0, 0)} for color in colors)


def test_apply_racing_red_frame_updates_mock_strip() -> None:
    strip = create_strip()
    strip.begin()

    apply_racing_red_frame(
        strip,
        2,
        light_count=2,
        make_color=lambda r, g, b: MockColor(r, g, b),
    )

    pixels = strip.pixels()
    assert pixels[2] == MockColor(255, 0, 0)
    assert pixels[7] == MockColor(255, 0, 0)
    assert pixels[0] == MockColor(0, 0, 0)


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
