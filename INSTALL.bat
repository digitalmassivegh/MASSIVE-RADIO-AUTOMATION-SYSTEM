@echo off
setlocal EnableDelayedExpansion
title MASSIVE RADIO AUTOMATION SYSTEM — Installer
cd /d "%~dp0"

echo.
echo  ================================================================
echo   MASSIVE RADIO AUTOMATION SYSTEM
echo   Windows Installer — please wait while we set everything up
echo  ================================================================
echo.

:: ────────────────────────────────────────────────────────────────────────────
:: STEP 1 — Detect Python
:: ────────────────────────────────────────────────────────────────────────────
set "PYTHON_EXE="

:: Try python in PATH first
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('where python 2^>nul') do (
        if not defined PYTHON_EXE set "PYTHON_EXE=%%i"
    )
)

:: Check common install locations if PATH lookup failed
if not defined PYTHON_EXE (
    for %%P in (
        "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        "%PROGRAMFILES%\Python313\python.exe"
        "%PROGRAMFILES%\Python312\python.exe"
        "%PROGRAMFILES%\Python311\python.exe"
        "%PROGRAMFILES%\Python310\python.exe"
    ) do (
        if exist %%P (
            if not defined PYTHON_EXE set "PYTHON_EXE=%%~P"
        )
    )
)

if defined PYTHON_EXE (
    echo  [OK]  Python found: !PYTHON_EXE!
    goto :INSTALL_APP
)

:: ────────────────────────────────────────────────────────────────────────────
:: STEP 2 — Python not found — download it automatically
:: ────────────────────────────────────────────────────────────────────────────
echo  [INFO] Python is not installed on this computer.
echo  [INFO] Downloading Python 3.11 automatically...
echo  [INFO] This requires an internet connection and takes about 1 minute.
echo.

:: Use PowerShell to download Python installer
set "PY_INSTALLER=%TEMP%\python_setup_mras.exe"
set "PY_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"

:: Check if 64-bit Windows
if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    if not defined PROCESSOR_ARCHITEW6432 (
        set "PY_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9.exe"
    )
)

echo  Downloading Python 3.11...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ProgressPreference='SilentlyContinue'; ^
   try { ^
     Invoke-WebRequest -Uri '%PY_URL%' -OutFile '%PY_INSTALLER%' -UseBasicParsing; ^
     Write-Host '  Download complete.' ^
   } catch { ^
     Write-Host ('  DOWNLOAD FAILED: ' + $_.Exception.Message); ^
     exit 1 ^
   }"

if not exist "%PY_INSTALLER%" (
    echo.
    echo  [ERROR] Could not download Python.
    echo.
    echo  Please install Python manually:
    echo    1. Open your browser and go to: https://www.python.org/downloads/
    echo    2. Click "Download Python 3.11"
    echo    3. Run the installer — TICK "Add Python to PATH"
    echo    4. Run this INSTALL.bat again after Python is installed
    echo.
    pause
    exit /b 1
)

echo  Installing Python 3.11 (this takes about 30 seconds)...
"%PY_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=1
if errorlevel 1 (
    echo.
    echo  [ERROR] Python installation failed (exit code %errorlevel%).
    echo  Please install Python 3.11 manually from https://www.python.org/downloads/
    echo  Tick "Add Python to PATH" during setup, then run this file again.
    echo.
    pause
    exit /b 1
)

echo  [OK]  Python installed successfully!

:: Add common Python paths to this session's PATH so we can use it immediately
set "PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%"
set "PATH=%PROGRAMFILES%\Python311;%PROGRAMFILES%\Python311\Scripts;%PATH%"

:: Locate the newly installed python.exe
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%PROGRAMFILES%\Python311\python.exe"
) do (
    if exist %%P (
        if not defined PYTHON_EXE set "PYTHON_EXE=%%~P"
    )
)

if not defined PYTHON_EXE (
    :: Fallback — try PATH again
    python --version >nul 2>&1
    if not errorlevel 1 set "PYTHON_EXE=python"
)

if not defined PYTHON_EXE (
    echo.
    echo  [ERROR] Python was installed but could not be found.
    echo  Please close this window, open a new Command Prompt, and run INSTALL.bat again.
    echo.
    pause
    exit /b 1
)

:: ────────────────────────────────────────────────────────────────────────────
:: STEP 3 — Run the Python installer (creates venv + installs deps)
:: ────────────────────────────────────────────────────────────────────────────
:INSTALL_APP
echo.
echo  [INFO] Installing Python dependencies (2-5 minutes on first run)...
echo  [INFO] Please wait — do not close this window.
echo.

"!PYTHON_EXE!" install.py --silent
if errorlevel 1 (
    echo.
    echo  [ERROR] Dependency installation failed.
    echo  See the output above for details.
    echo  Common fix: run this file as Administrator (right-click → Run as administrator)
    echo.
    pause
    exit /b 1
)

:: ────────────────────────────────────────────────────────────────────────────
:: STEP 4 — Create desktop shortcut
:: ────────────────────────────────────────────────────────────────────────────
echo.
echo  [INFO] Creating desktop shortcut...

set "APP_DIR=%~dp0"
set "APP_DIR=!APP_DIR:~0,-1!"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws  = New-Object -ComObject WScript.Shell; ^
   $lnk = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Massive Radio.lnk'); ^
   $lnk.TargetPath     = '!APP_DIR!\START.bat'; ^
   $lnk.WorkingDirectory = '!APP_DIR!'; ^
   $lnk.Description    = 'MASSIVE RADIO AUTOMATION SYSTEM'; ^
   $lnk.Save(); ^
   Write-Host '[OK]  Desktop shortcut created: Massive Radio'"

:: Start Menu shortcut
set "SM=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Massive Radio"
if not exist "!SM!" mkdir "!SM!"
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws  = New-Object -ComObject WScript.Shell; ^
   $lnk = $ws.CreateShortcut('!SM!\Massive Radio Automation System.lnk'); ^
   $lnk.TargetPath     = '!APP_DIR!\START.bat'; ^
   $lnk.WorkingDirectory = '!APP_DIR!'; ^
   $lnk.Description    = 'MASSIVE RADIO AUTOMATION SYSTEM'; ^
   $lnk.Save(); ^
   Write-Host '[OK]  Start Menu shortcut created'"

:: ────────────────────────────────────────────────────────────────────────────
:: DONE
:: ────────────────────────────────────────────────────────────────────────────
echo.
echo  ================================================================
echo   Installation complete!
echo.
echo   To start: double-click "Massive Radio" on your Desktop
echo          or double-click START.bat in this folder
echo  ================================================================
echo.
pause
