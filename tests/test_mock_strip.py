from kano_ring import create_strip, is_mock_mode
from kano_ring.strip import MockColor, MockPixelStrip


def test_create_strip_uses_mock_in_cloud() -> None:
    strip = create_strip()
    assert is_mock_mode()
    assert isinstance(strip, MockPixelStrip)


def test_mock_strip_pixel_operations() -> None:
    strip = create_strip()
    strip.begin()

    red = MockColor(255, 0, 0)
    strip.setPixelColor(0, red)
    strip.show()

    assert strip.pixels()[0] == red
    assert strip.pixels()[1] == MockColor(0, 0, 0)


def test_mock_strip_rejects_out_of_range_index() -> None:
    strip = create_strip()
    strip.begin()

    try:
        strip.setPixelColor(99, MockColor(0, 0, 0))
        raised = False
    except IndexError:
        raised = True

    assert raised
