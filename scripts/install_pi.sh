#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! python3 -c "import ensurepip" >/dev/null 2>&1; then
  echo "Missing venv support. Install it first:"
  echo "  sudo apt update && sudo apt install -y python3-venv python3-full"
  exit 1
fi

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements-pi.txt
.venv/bin/pip install -e .

echo
echo "Pi install complete."
echo "Run hardware scripts with sudo and the venv Python:"
echo "  sudo .venv/bin/python3 scripts/turn_off_leds.py"
echo "  sudo .venv/bin/python3 scripts/rainbow_demo.py"
