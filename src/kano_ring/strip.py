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


def _resolve_strip_type(name: str | None):
    """Map a short name to an rpi_ws281x strip_type constant, or None for default."""
    if name is None:
        return None

    # Imported only when building a real strip.
    import rpi_ws281x as ws  # type: ignore[import-untyped]

    key = name.strip().lower()
    mapping = {
        "grb": ws.WS2811_STRIP_GRB,
        "rgb": ws.WS2811_STRIP_RGB,
        "gbr": ws.WS2811_STRIP_GBR,
        "rgbw": getattr(ws, "SK6812_STRIP_RGBW", None),
    }
    if key not in mapping or mapping[key] is None:
        known = ", ".join(sorted(k for k, v in mapping.items() if v is not None))
        raise ValueError(f"Unknown strip type {name!r}; expected one of: {known}")
    return mapping[key]


def create_strip(config: KanoRingConfig | None = None) -> PixelStripProtocol:
    """Create a real or mock PixelStrip depending on available hardware.

    Real-hardware construction mirrors Kano's ``KanoHatLeds``: count, pin,
    and ``dma=10``, with brightness applied via the constructor (equivalent
    to their ``setBrightness`` call before ``begin``).
    """
    global _MOCK_MODE

    cfg = config or KanoRingConfig.from_env()

    try:
        # Adafruit_NeoPixel is the name Kano imported; it is an alias for PixelStrip.
        from rpi_ws281x import Adafruit_NeoPixel  # type: ignore[import-untyped]
    except Exception:
        _MOCK_MODE = True
        return MockPixelStrip(cfg)

    _MOCK_MODE = False
    strip_kwargs: dict = {
        "num": cfg.led_count,
        "pin": cfg.led_pin,
        "freq_hz": cfg.led_freq_hz,
        "dma": cfg.led_dma,
        "invert": cfg.led_invert,
        "brightness": cfg.led_brightness,
        "channel": cfg.led_channel,
    }
    strip_type = _resolve_strip_type(cfg.strip_type)
    if strip_type is not None:
        strip_kwargs["strip_type"] = strip_type

    # Prefer keyword args (as in KanoHatLeds) so dma/brightness stay unambiguous.
    return Adafruit_NeoPixel(**strip_kwargs)
