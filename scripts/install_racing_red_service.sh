#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UNIT_NAME="kano-racing-red.service"
TEMPLATE="$ROOT/systemd/$UNIT_NAME"
DEST="/etc/systemd/system/$UNIT_NAME"

if [ ! -f "$TEMPLATE" ]; then
  echo "Service template not found: $TEMPLATE"
  exit 1
fi

if [ ! -x "$ROOT/.venv/bin/python3" ]; then
  echo "Missing .venv. Run ./scripts/install_pi.sh first."
  exit 1
fi

if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root (use sudo)."
  exit 1
fi

sed "s|@REPO_ROOT@|${ROOT}|g" "$TEMPLATE" >"$DEST"
chmod 644 "$DEST"

systemctl daemon-reload
systemctl enable "$UNIT_NAME"

echo
echo "Installed and enabled $UNIT_NAME"
echo
echo "Start now:   sudo systemctl start $UNIT_NAME"
echo "View logs:   sudo journalctl -u $UNIT_NAME -f"
echo "Stop:        sudo systemctl stop $UNIT_NAME"
echo "Disable:     sudo systemctl disable $UNIT_NAME"
echo "Remove unit: sudo rm $DEST && sudo systemctl daemon-reload"
