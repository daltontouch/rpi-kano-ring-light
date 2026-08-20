"""Ensure src/ is importable when scripts are run directly."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if _SRC.is_dir():
    src_path = str(_SRC)
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
