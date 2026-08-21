#!/usr/bin/env python3
"""Chase a yellow-to-red sunset gradient around the Kano ring until stopped (Ctrl+C)."""

import _bootstrap  # noqa: F401

from kano_ring import create_strip, is_mock_mode
from kano_ring.chasing_sunset import run_chasing_sunset


def main() -> None:
    strip = create_strip()
    mode = "mock" if is_mock_mode() else "hardware"
    print(f"Chasing sunset ({mode} mode). Press Ctrl+C to stop.")
    run_chasing_sunset(strip)
    print("Stopped.")


if __name__ == "__main__":
    main()
