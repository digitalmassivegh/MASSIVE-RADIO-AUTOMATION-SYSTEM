#!/usr/bin/env bash
# MASSIVE RADIO AUTOMATION SYSTEM — macOS Installer
# Double-click this file in Finder to install.
# If macOS blocks it: right-click → Open → Open

# Change to the directory this script lives in
cd "$(dirname "$0")"

echo ""
echo "  ╔══════════════════════════════════════════════════════╗"
echo "  ║       MASSIVE RADIO AUTOMATION SYSTEM               ║"
echo "  ║       macOS Installer                                ║"
echo "  ╚══════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "  Python 3 was not found on your Mac."
    echo ""
    echo "  Please install it from:"
    echo "  https://www.python.org/downloads/"
    echo ""
    echo "  Or via Homebrew:  brew install python"
    echo ""
    open "https://www.python.org/downloads/"
    read -p "  Press Enter to close..."
    exit 1
fi

PY_VER=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $PY_VER"
echo ""
echo "  Running installer... (this may take a few minutes on first run)"
echo ""

python3 install.py
read -p "  Press Enter to close..."
