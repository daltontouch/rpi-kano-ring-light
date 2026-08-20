from __future__ import annotations

from typing import Protocol

from kano_ring.config import KanoRingConfig

_MOCK_MODE = False


class PixelStripProtocol(Protocol):
    def begin(self) -> None: ...

    def numPixels(self) -> int: ...

    def setPixelColor(self, index: int, color: object) -> None: ...

    def show(self) -> None: ...


class MockColor:
    """Minimal Color stand-in matching rpi_ws281x's (R, G, B) constructor."""

    __slots__ = ("r", "g", "b")

    def __init__(self, r: int, g: int, b: int) -> None:
        self.r = r
        self.g = g
        self.b = b

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MockColor):
            return NotImplemented
        return (self.r, self.g, self.b) == (other.r, other.g, other.b)

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"


class MockPixelStrip:
    """In-memory LED strip for development without Raspberry Pi hardware."""

    def __init__(self, config: KanoRingConfig) -> None:
        self._config = config
        self._pixels: list[MockColor] = [
            MockColor(0, 0, 0) for _ in range(config.led_count)
        ]
        self._initialized = False

    def begin(self) -> None:
        self._initialized = True

    def numPixels(self) -> int:
        return len(self._pixels)

    def setPixelColor(self, index: int, color: MockColor) -> None:
        if not 0 <= index < len(self._pixels):
            raise IndexError(f"LED index {index} out of range (0-{len(self._pixels) - 1})")
        self._pixels[index] = color

    def show(self) -> None:
        if not self._initialized:
            raise RuntimeError("Call begin() before show()")

    def pixels(self) -> list[MockColor]:
        return list(self._pixels)


def is_mock_mode() -> bool:
    return _MOCK_MODE


def create_strip(config: KanoRingConfig | None = None) -> PixelStripProtocol:
    """Create a real or mock PixelStrip depending on available hardware."""
    global _MOCK_MODE

    cfg = config or KanoRingConfig()

    try:
        from rpi_ws281x import PixelStrip  # type: ignore[import-untyped]

        _MOCK_MODE = False
        return PixelStrip(
            cfg.led_count,
            cfg.led_pin,
            cfg.led_freq_hz,
            cfg.led_dma,
            cfg.led_invert,
            cfg.led_brightness,
            cfg.led_channel,
        )
    except Exception:
        _MOCK_MODE = True
        return MockPixelStrip(cfg)
