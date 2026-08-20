"""Kano light ring control with automatic mock fallback for off-device development."""

from kano_ring.config import KanoRingConfig
from kano_ring.strip import create_strip, is_mock_mode

__all__ = ["KanoRingConfig", "create_strip", "is_mock_mode"]
