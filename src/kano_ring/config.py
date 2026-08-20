from dataclasses import dataclass


@dataclass(frozen=True)
class KanoRingConfig:
    """Hardware settings for the Kano Computer Kit light ring."""

    led_count: int = 10
    led_pin: int = 18
    led_freq_hz: int = 800_000
    led_dma: int = 10
    led_brightness: int = 255
    led_invert: bool = False
    led_channel: int = 0
