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
echo
echo "Option A — activate the venv, then run with sudo:"
echo "  source .venv/bin/activate"
echo "  sudo python3 scripts/rainbow_demo.py"
echo
echo "Option B — call the venv Python directly:"
echo "  sudo .venv/bin/python3 scripts/rainbow_demo.py"
echo
echo "Option C — wrapper script:"
echo "  sudo ./scripts/run_pi.sh scripts/rainbow_demo.py"
