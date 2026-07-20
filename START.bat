@echo off
setlocal EnableDelayedExpansion
title MASSIVE RADIO AUTOMATION SYSTEM
cd /d "%~dp0"

:: ── Verify installed ─────────────────────────────────────────────────────────
if not exist "venv\Scripts\python.exe" (
    echo.
    echo  MASSIVE RADIO AUTOMATION SYSTEM is not installed yet.
    echo  Please run INSTALL.bat first.
    echo.
    pause
    exit /b 1
)

:: ── Launch ───────────────────────────────────────────────────────────────────
echo.
echo  Starting MASSIVE RADIO AUTOMATION SYSTEM...
echo.
venv\Scripts\python.exe main.py
