#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -x .venv/bin/python3 ]; then
  echo "Missing .venv. Run ./scripts/install_pi.sh first."
  exit 1
fi

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <script.py> [args...]"
  echo "Example: sudo $0 scripts/rainbow_demo.py"
  exit 1
fi

SCRIPT="$1"
shift

if [ ! -f "$SCRIPT" ]; then
  echo "Script not found: $SCRIPT"
  exit 1
fi

exec sudo .venv/bin/python3 "$SCRIPT" "$@"
