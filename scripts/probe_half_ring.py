#!/usr/bin/env python3
"""Diagnose a half-lit Kano ring: which indices and which GPIO respond.

Lights indices 0-4 red and 5-9 blue so you can see *which* half works.
Then optionally probes GPIO 21 (PCM, avoids audio/PWM clash) and a
dual-pin 5+5 layout some community posts suspect.

On a Pi::

    sudo .venv/bin/python3 scripts/probe_half_ring.py
    sudo .venv/bin/python3 scripts/probe_half_ring.py --phase dual
    sudo .venv/bin/python3 scripts/probe_half_ring.py --phase pin21

If only red (0-4) ever lights on pin 18, the daisy-chain or power after
LED 4 is likely open — software cannot repair that.
"""

from __future__ import annotations

import _bootstrap  # noqa: F401

import argparse
import time

from kano_ring import KanoRingConfig, create_strip, is_mock_mode
from kano_ring.strip import MockColor


def _color(r: int, g: int, b: int):
    if is_mock_mode():
        return MockColor(r, g, b)
    from rpi_ws281x import Color  # type: ignore[import-untyped]

    return Color(r, g, b)


def _clear(strip) -> None:
    off = _color(0, 0, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, off)
    strip.show()


def _hold(seconds: float, message: str) -> None:
    print(message)
    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        raise


def phase_split_colors(cfg: KanoRingConfig, hold: float) -> None:
    """0-4 red, 5-9 blue — identifies which index range is alive."""
    strip = create_strip(cfg)
    strip.begin()
    n = strip.numPixels()
    print(
        f"\n=== split colors on GPIO {cfg.led_pin} ===\n"
        f"numPixels()={n}, brightness={cfg.led_brightness}, "
        f"dma={cfg.led_dma}, mock={is_mock_mode()}"
    )
    split = n // 2
    red = _color(255, 0, 0)
    blue = _color(0, 0, 255)
    for i in range(n):
        strip.setPixelColor(i, red if i < split else blue)
    strip.show()
    _hold(
        hold,
        f"Indices 0-{split - 1} = RED, {split}-{n - 1} = BLUE.\n"
        "  Only red  = lower indices respond.\n"
        "  Only blue = upper indices respond.\n"
        "  Both colors = full configured count is addressable.\n"
        "  Mixed/dim = signal or power issue.",
    )
    _clear(strip)


def phase_pin(pin: int, count: int, rgb: tuple[int, int, int], hold: float) -> None:
    cfg = KanoRingConfig.from_env()
    cfg = KanoRingConfig(
        led_count=count,
        led_pin=pin,
        led_freq_hz=cfg.led_freq_hz,
        led_dma=cfg.led_dma,
        led_brightness=cfg.led_brightness,
        led_invert=cfg.led_invert,
        led_channel=0 if pin in (12, 18) else 0,
        strip_type=cfg.strip_type,
    )
    print(f"\n=== solid fill GPIO {pin}, count={count}, color={rgb} ===")
    try:
        strip = create_strip(cfg)
        strip.begin()
    except Exception as exc:
        print(f"FAILED to init GPIO {pin}: {exc}")
        return

    color = _color(*rgb)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    _hold(hold, f"All {strip.numPixels()} buffer slots set on GPIO {pin}. Observe the ring.")
    _clear(strip)


def phase_dual(hold: float) -> None:
    """Drive 5 LEDs on GPIO 18 (PWM) and 5 on GPIO 21 (PCM) at once."""
    try:
        from rpi_ws281x import Adafruit_NeoPixel, Color  # type: ignore[import-untyped]
    except Exception as exc:
        print(f"rpi_ws281x unavailable ({exc}); dual probe needs a Pi.")
        return

    print("\n=== dual strip: GPIO18 x5 red + GPIO21 x5 blue ===")
    print("If the dark half lights blue, that half is wired to GPIO 21.")

    brightness = KanoRingConfig.from_env().led_brightness
    strip_a = Adafruit_NeoPixel(5, 18, dma=10, brightness=brightness, channel=0)
    # GPIO 21 uses PCM; use a different DMA channel to avoid clashing with strip_a.
    strip_b = Adafruit_NeoPixel(5, 21, dma=11, brightness=brightness, channel=0)

    try:
        strip_a.begin()
        strip_b.begin()
    except Exception as exc:
        print(f"FAILED dual begin: {exc}")
        return

    red = Color(255, 0, 0)
    blue = Color(0, 0, 255)
    for i in range(5):
        strip_a.setPixelColor(i, red)
        strip_b.setPixelColor(i, blue)
    strip_a.show()
    strip_b.show()
    _hold(hold, "GPIO18 half should be red; GPIO21 half should be blue (if wired).")

    for i in range(5):
        strip_a.setPixelColor(i, Color(0, 0, 0))
        strip_b.setPixelColor(i, Color(0, 0, 0))
    strip_a.show()
    strip_b.show()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phase",
        choices=("split", "pin21", "dual", "all"),
        default="all",
        help="Which probe to run (default: all)",
    )
    parser.add_argument("--hold", type=float, default=8.0, help="Seconds to hold each pattern")
    args = parser.parse_args()

    cfg = KanoRingConfig.from_env()
    print(
        f"Config: pin={cfg.led_pin} count={cfg.led_count} "
        f"brightness={cfg.led_brightness} dma={cfg.led_dma} "
        f"strip_type={cfg.strip_type or 'default'}"
    )
    print(
        "Tip: if PWM audio is enabled, add dtparam=audio=off to "
        "/boot/firmware/config.txt (or /boot/config.txt) and reboot."
    )

    try:
        if args.phase in ("split", "all"):
            phase_split_colors(cfg, args.hold)
        if args.phase in ("pin21", "all"):
            phase_pin(21, 10, (0, 255, 0), args.hold)
        if args.phase in ("dual", "all"):
            phase_dual(args.hold)
    except KeyboardInterrupt:
        print("\nInterrupted.")
    print("Done.")


if __name__ == "__main__":
    main()
