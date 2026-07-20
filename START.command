#!/usr/bin/env bash
# MASSIVE RADIO AUTOMATION SYSTEM — macOS Launcher
# Double-click in Finder to start.
# If macOS blocks it: right-click → Open → Open

cd "$(dirname "$0")"

if [ ! -f "venv/bin/python" ]; then
    echo ""
    echo "  The application is not installed yet."
    echo "  Please double-click INSTALL.command first."
    echo ""
    read -p "  Press Enter to close..."
    exit 1
fi

echo ""
echo "  Starting MASSIVE RADIO AUTOMATION SYSTEM..."
echo ""
venv/bin/python main.py
read -p "  Press Enter to close..."
