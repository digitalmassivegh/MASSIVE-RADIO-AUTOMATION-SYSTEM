#!/usr/bin/env bash
# MASSIVE RADIO AUTOMATION SYSTEM — Linux Installer
# Run once:  bash install.sh

cd "$(dirname "$0")"

echo ""
echo "  ╔══════════════════════════════════════════════════════╗"
echo "  ║       MASSIVE RADIO AUTOMATION SYSTEM               ║"
echo "  ║       Linux Installer                                ║"
echo "  ╚══════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "  Python 3 is not installed."
    echo ""
    echo "  Install it with:"
    echo "    Ubuntu/Debian:  sudo apt install python3 python3-pip python3-venv"
    echo "    Fedora:         sudo dnf install python3"
    echo "    Arch:           sudo pacman -S python"
    echo ""
    exit 1
fi

PY_VER=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $PY_VER"
echo ""
echo "  Running installer... (this may take a few minutes on first run)"
echo ""

python3 install.py
read -p "  Press Enter to close..."
