from __future__ import annotations

import os
from dataclasses import dataclass


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return int(raw)


@dataclass(frozen=True)
class KanoRingConfig:
    """Hardware settings for the Kano Computer Kit light ring.

    Defaults use 5 LEDs (working half of the physical 10-LED ring), GPIO 18,
    DMA 10, brightness 150. Override with env vars on a Pi:
    ``KANO_RING_COUNT``, ``KANO_RING_PIN``, ``KANO_RING_BRIGHTNESS``,
    ``KANO_RING_DMA``.
    """

    led_count: int = 5
    led_pin: int = 18
    led_freq_hz: int = 800_000
    led_dma: int = 10
    # KanoHatLeds default; full 255 can brown out later LEDs on Pi 5V.
    led_brightness: int = 150
    led_invert: bool = False
    led_channel: int = 0
    # None => library default (WS2811_STRIP_GRB). Set "rgb" / "grb" / "rgbw".
    strip_type: str | None = None

    @classmethod
    def from_env(cls) -> KanoRingConfig:
        """Build config from defaults plus optional environment overrides."""
        base = cls()
        return cls(
            led_count=_env_int("KANO_RING_COUNT", base.led_count),
            led_pin=_env_int("KANO_RING_PIN", base.led_pin),
            led_freq_hz=base.led_freq_hz,
            led_dma=_env_int("KANO_RING_DMA", base.led_dma),
            led_brightness=_env_int("KANO_RING_BRIGHTNESS", base.led_brightness),
            led_invert=base.led_invert,
            led_channel=base.led_channel,
            strip_type=os.environ.get("KANO_RING_STRIP_TYPE") or base.strip_type,
        )
