#!/usr/bin/env bash
# MASSIVE RADIO AUTOMATION SYSTEM — Linux Launcher
# Run:  bash start.sh

cd "$(dirname "$0")"

if [ ! -f "venv/bin/python" ]; then
    echo ""
    echo "  The application is not installed yet."
    echo "  Please run:  bash install.sh"
    echo ""
    exit 1
fi

echo ""
echo "  Starting MASSIVE RADIO AUTOMATION SYSTEM..."
echo ""
venv/bin/python main.py
