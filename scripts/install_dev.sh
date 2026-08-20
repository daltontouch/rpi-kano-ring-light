#!/usr/bin/env python3
"""Run the install script steps locally (same as .cursor/environment.json)."""

import subprocess
import sys


def main() -> int:
    commands = [
        [sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"],
        [sys.executable, "-m", "pip", "install", "--user", "-e", "."],
        [sys.executable, "-m", "pytest", "-q"],
    ]
    for command in commands:
        print(f"+ {' '.join(command)}")
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
