#!/usr/bin/env python3
"""Race red lights around the Kano ring until stopped (Ctrl+C)."""

import _bootstrap  # noqa: F401

from kano_ring import create_strip, is_mock_mode
from kano_ring.racing_red import run_racing_red


def main() -> None:
    strip = create_strip()
    mode = "mock" if is_mock_mode() else "hardware"
    print(f"Racing red lights ({mode} mode). Press Ctrl+C to stop.")
    run_racing_red(strip)
    print("Stopped.")


if __name__ == "__main__":
    main()
