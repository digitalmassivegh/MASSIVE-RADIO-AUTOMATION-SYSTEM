@echo off
REM ============================================================================
REM MASSIVE RADIO AUTOMATION SYSTEM - Windows Setup Script
REM ============================================================================
REM This script installs all dependencies and runs the application
REM ============================================================================

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                MASSIVE RADIO AUTOMATION SYSTEM                         ║
echo ║                     Windows Setup Script                               ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [✓] Python detected
python --version
echo.

REM Upgrade pip, setuptools, and wheel
echo [1/4] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip
    pause
    exit /b 1
)
echo [✓] Pip upgraded
echo.

REM Install pygame (pre-release version for better compatibility)
echo [2/4] Installing pygame (this may take a few minutes)...
pip install --pre pygame
if errorlevel 1 (
    echo [WARNING] pygame pre-release failed, trying stable version...
    pip install pygame
    if errorlevel 1 (
        echo [ERROR] Failed to install pygame
        echo Try installing build tools: https://visualstudio.microsoft.com/downloads/
        pause
        exit /b 1
    )
)
echo [✓] Pygame installed
echo.

REM Install all requirements
echo [3/4] Installing all dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    pause
    exit /b 1
)
echo [✓] All dependencies installed
echo.

REM Success message
echo [4/4] Setup complete!
echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                    Setup Successful!                                   ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo Starting MASSIVE RADIO AUTOMATION SYSTEM...
echo.

REM Run the application
python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application failed to start
    echo Check the error messages above
    pause
)

exit /b 0
