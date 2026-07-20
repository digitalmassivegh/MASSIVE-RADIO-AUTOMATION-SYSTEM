# Radio Studio — Build & Deployment Guide

## Overview

Radio Studio has two components:

| Component | Tech | Where it runs |
|---|---|---|
| **Desktop App** | Python / PyQt5 / pygame | DJ's local Windows or macOS machine |
| **API Server** | Python / FastAPI | Replit (always-on cloud) |

---

## 1. Running from Source (all platforms)

### Prerequisites

- Python 3.8 or newer
- pip (comes with Python)
- PortAudio (Linux / macOS only — for microphone input)

### Windows

```cmd
# 1. Open a command prompt in the RadioStudio folder
setup.bat        # installs all Python dependencies
run_source.bat   # launches the desktop app
```

### macOS

```bash
bash setup.sh    # installs dependencies (requires Homebrew for PortAudio)
bash run.sh      # launches the desktop app
# or double-click run.command in Finder
```

### Linux

```bash
bash setup.sh    # installs apt packages + Python dependencies
bash run.sh      # launches the desktop app
```

---

## 2. Building a Standalone Binary (PyInstaller)

A standalone binary bundles Python and all dependencies — **no Python installation needed** on the end-user machine.

> **Important:** You must build on the same OS as your target platform.
> - Windows binary → build on Windows
> - macOS binary   → build on macOS
> - Linux binary   → build on Linux

### Prerequisites

```bash
pip install pyinstaller
pip install -r requirements.txt
```

### Build

```bash
cd radio_studio/build
python build.py
```

Output will be at `dist/RadioStudio/` with a `RadioStudio.zip` archive.

### What the Build Creates

```
dist/
  RadioStudio/
    RadioStudio.exe      ← Windows executable (or RadioStudio on macOS/Linux)
    _internal/           ← bundled Python + all dependencies
    run.bat              ← Windows launcher (double-click)
    run.sh               ← macOS/Linux launcher
    run.command          ← macOS Finder launcher (double-click)
    README.md
    BUILD_INSTRUCTIONS.md
  RadioStudio.zip        ← ready to distribute
```

### macOS Code Signing (optional)

```bash
codesign --deep --force --sign "Developer ID Application: Your Name (TEAMID)" \
  dist/RadioStudio/RadioStudio
```

For Gatekeeper-friendly distribution, sign and notarise via Apple's notarytool.

### Windows Code Signing (optional)

```cmd
signtool sign /a /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 ^
  dist\RadioStudio\RadioStudio.exe
```

---

## 3. API Server (Replit)

The API server runs on Replit and is already configured via the `Radio Studio API` workflow.

### Manual start

```bash
cd radio_studio
python run_api_server.py
```

### Environment variables / secrets

Set these in Replit Secrets:

| Key | Description |
|---|---|
| `SESSION_SECRET` | Random 32-char string for JWT signing |

### First admin user

The API uses JWT auth. Create the first admin account:

```bash
cd radio_studio
python -c "
from api_server.database import init_db, create_user
init_db()
create_user('admin', 'your-password', role='admin')
print('Admin created.')
"
```

---

## 4. Connecting Desktop to Server

1. Launch the desktop app
2. Open the **Sync** tab → click the server URL field
3. Enter your Replit API URL (e.g. `https://yourname.replit.app`)
4. Sign in with username + password — the app fetches a JWT automatically
5. The sync engine will start pulling stories, tracks, and schedule from the server

---

## 5. System Requirements

### Desktop App

| | Minimum | Recommended |
|---|---|---|
| OS | Windows 10, macOS 11, Ubuntu 20.04 | Windows 11, macOS 13, Ubuntu 22.04 |
| RAM | 512 MB | 2 GB |
| CPU | Any dual-core | Quad-core for audio processing |
| Audio | Standard output | Professional audio interface |
| Python | 3.8 | 3.11 |

### Linux extras

```bash
sudo apt install libportaudio2 portaudio19-dev
```

---

## 6. File Locations (runtime)

| File | Location |
|---|---|
| Config | `config.json` (next to executable) |
| Local database | `data/studio.db` |
| Media library | `media/` (configurable in Settings) |
| As-run CSV logs | `logs/asrun_YYYY-MM-DD.csv` |
| Server database | `data/server.db` (Replit side) |

---

## 7. Troubleshooting

**Audio not working on Linux:**
```bash
sudo apt install libportaudio2
```

**PyQt5 import error:**
```bash
pip install PyQt5==5.15.10
```

**`no module named pygame`:**
```bash
pip install pygame==2.5.2
```

**Sync not connecting:**
- Check the API URL in Sync settings (no trailing slash)
- Verify the API server workflow is running on Replit
- Check `SESSION_SECRET` is set in Replit Secrets

**Build fails with UPX error:**
```bash
python build.py  # UPX is optional; build still succeeds without it
```
