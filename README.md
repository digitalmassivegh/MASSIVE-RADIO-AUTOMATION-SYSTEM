# 🎙️ MASSIVE RADIO AUTOMATION SYSTEM

**Professional radio station automation software** with desktop GUI, cloud sync, commercial scheduling, and live microphone support.

---

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Development](#development)
- [Support](#support)

---

## ✨ Features

### Phase 1: Desktop Application
- 🎵 **Audio Playback** - PyQt5 GUI with dual-deck management
- 🔄 **Sync Engine** - Background daemon for cloud synchronization
- 🎚️ **Volume Control** - Real-time level adjustment

### Phase 2: Web API Server
- 🌐 **FastAPI** - RESTful API for remote control
- 🔐 **JWT Authentication** - Secure token-based access
- 📁 **File Upload** - Cloud media library management

### Phase 3: Web Dashboard
- 📊 **Admin Panel** - Real-time monitoring and control
- 📱 **Responsive Design** - Works on desktop and mobile

### Phase 4: Audio Intelligence
- 🔇 **Silence Detection** - Automatic ad insertion
- 📈 **Audio Normalization** - Consistent levels across tracks
- 🎬 **Commercial Scheduling** - Automated break management

### Phase 5: Live Microphone
- 🎙️ **Low-Latency Capture** - Real-time talkover support
- 📉 **Auto-Ducking** - Background music volume control
- 🔊 **Passthrough Monitoring** - Headphone preview

### Compliance
- 📝 **As-Run Logger** - Broadcast compliance documentation
- 📅 **Schedule Management** - Commercial tracking
- 📋 **Export Reports** - CSV/JSON format

---

## 🖥️ System Requirements

### Minimum
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: 3.9, 3.10, or 3.11
- **RAM**: 4GB
- **Disk**: 2GB free space

### Recommended
- **CPU**: Quad-core or better
- **RAM**: 8GB+
- **Disk**: SSD with 10GB+ free space
- **Audio Interface**: USB audio interface for microphone input

### Optional Dependencies
- **PortAudio**: Required for microphone support
- **FFmpeg**: For advanced audio processing (future phases)

---

## 🚀 Quick Start

### Windows

1. **Download** `setup.bat` from the repository
2. **Place it** in your project folder
3. **Double-click** `setup.bat`
4. ✅ Done! The app will launch automatically

### macOS / Linux

```bash
# Clone the repository
git clone https://github.com/digitalmassivegh/MASSIVE-RADIO-AUTOMATION-SYSTEM.git
cd MASSIVE-RADIO-AUTOMATION-SYSTEM

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 📦 Installation

### Prerequisites

Ensure you have Python 3.9+ installed:

```bash
python --version
```

### Install System Dependencies

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y python3-dev libsdl2-dev libsdl2-image-dev \
  libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev portaudio19-dev
```

#### macOS
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf freetype portaudio
```

#### Windows
- Download [PortAudio](http://portaudio.com/download.html)
- Follow installation wizard

### Install Python Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt
```

### Verify Installation

```bash
# Test imports
python -c "import pygame; print('✓ pygame')"
python -c "import PyQt5; print('✓ PyQt5')"
python -c "import fastapi; print('✓ FastAPI')"
```

---

## 🎯 Usage

### Start the Desktop Application

```bash
python main.py
```

The application will:
1. Initialize the SQLite database (auto-created on first run)
2. Load configuration from `config.json`
3. Initialize pygame audio mixer
4. Open the main GUI window
5. Start background sync engine

**Output:**
```
[MASSIVE RADIO] System ready.
[MASSIVE RADIO] Local database  : ./studio.db
[MASSIVE RADIO] Media folder    : ./media
[MASSIVE RADIO] As-run logs     : ./logs
[MASSIVE RADIO] API server URL  : http://localhost:8000
[MASSIVE RADIO] Sync enabled    : True
[MASSIVE RADIO] Microphone      : Available
```

### Start the Web API Server (Separate Process)

```bash
python run_api_server.py
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Configuration

Edit `config.json` to customize:

```json
{
  "db_path": "./studio.db",
  "media_folder": "./media",
  "api_url": "http://localhost:8000",
  "sync_enabled": true,
  "sync_interval": 60
}
```

---

## 🏗️ Architecture

### Directory Structure

```
MASSIVE-RADIO-AUTOMATION-SYSTEM/
├── main.py                 # Desktop app entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── setup.bat             # Windows setup script
│
├── audio/
│   ├── player.py         # AudioEngine - playback control
│   ├── processor.py      # AudioProcessor - silence detection
│   ├── auto_player.py    # AutoPlayer - queue management
│   └── mic_engine.py     # MicEngine - microphone capture
│
├── db/
│   ├── local_db.py       # SQLite database layer
│   └── schema.py         # Database schema
│
├── sync/
│   └── sync_engine.py    # Background sync daemon
│
├── commercial/
│   ├── scheduler.py      # CommercialScheduler - ad breaks
│   └── asrun_logger.py   # AsRunLogger - compliance
│
├── ui/
│   ├── main_window.py    # MainWindow - GUI
│   ├── styles.py         # Dark theme stylesheet
│   └── logo.png          # Branding
│
├── api/
│   └── server.py         # FastAPI web server
│
├── logs/                 # As-run compliance logs
└── media/               # Audio file library
```

### Data Flow

```
┌─────────────────────┐
│   Desktop GUI       │
│   (PyQt5)           │
└──────────┬──────────┘
           │
           ├─────→ AudioEngine ──→ Speakers/Headphones
           │
           ├─────→ AudioProcessor ──→ Silence Detection
           │
           ├─────→ AutoPlayer ──→ Dual Decks
           │
           ├─────→ MicEngine ──→ Microphone Input
           │
           ├─────→ SyncEngine ──→ Cloud API
           │
           ├─────→ CommercialScheduler ──→ Ad Breaks
           │
           └─────→ AsRunLogger ──→ Compliance Logs

┌──────────────────────┐
│  Web API Server      │
│  (FastAPI)           │
└──────────┬───────────┘
           │
           ├─────→ Authentication (JWT)
           ├─────→ Media Management
           ├─────→ Remote Control
           └─────→ Dashboard
```

---

## 🔧 Development

### Running Tests

Tests are automatically run on every push via GitHub Actions:

```bash
# View test results
# → Go to https://github.com/digitalmassivegh/MASSIVE-RADIO-AUTOMATION-SYSTEM/actions
```

#### Local Testing

```bash
# Install dev dependencies
pip install pytest pytest-cov flake8 bandit

# Run syntax checks
flake8 . --max-line-length=127

# Security audit
bandit -r . -ll

# Run tests (when available)
pytest
```

### Code Quality

The project uses:
- **flake8** - Code style (PEP 8)
- **bandit** - Security vulnerability scanning
- **pytest** - Unit testing framework

---

## 🔄 Continuous Integration

### GitHub Actions Workflow

Every push triggers automated builds across:

| OS | Python Versions |
|----|-----------------|
| Ubuntu | 3.9, 3.10, 3.11 |
| Windows | 3.9, 3.10, 3.11 |
| macOS | 3.9, 3.10, 3.11 |

**Checks performed:**
- ✅ Dependencies installation
- ✅ Module imports verification
- ✅ Python syntax validation
- ✅ Code style (flake8)
- ✅ Security scanning (bandit)
- ✅ Automatic release generation

**View results:** https://github.com/digitalmassivegh/MASSIVE-RADIO-AUTOMATION-SYSTEM/actions

---

## 📝 Configuration Files

### `config.json` (Auto-generated on first run)

```json
{
  "db_path": "./studio.db",
  "media_folder": "./media",
  "api_url": "http://localhost:8000",
  "sync_enabled": true,
  "sync_interval": 60,
  "log_level": "INFO"
}
```

### `requirements.txt`

Locked dependencies for reproducible builds. Update with:

```bash
pip freeze > requirements.txt
```

---

## 🐛 Troubleshooting

### Issue: "pygame not found"

**Solution:**
```bash
pip install --pre pygame
# or
pip install pygame==2.1.3
```

### Issue: "PyQt5 display error" (Linux)

**Solution:**
```bash
sudo apt-get install python3-pyqt5
```

### Issue: "PortAudio not found" (Microphone unavailable)

**Solution:**
- **Windows**: Download from http://portaudio.com/download.html
- **macOS**: `brew install portaudio`
- **Linux**: `sudo apt-get install portaudio19-dev`

### Issue: "Database locked"

**Solution:** Close other instances of the application. SQLite only allows one write connection.

### Issue: Workflow failing on GitHub

**View logs:**
1. Go to **Actions** tab
2. Click the failing workflow run
3. Expand the failed job for detailed error messages

---

## 📚 Documentation

- **Desktop App**: Launch with `python main.py`
- **Web API**: Visit http://localhost:8000/docs (Swagger UI)
- **Configuration**: Edit `config.json`
- **Database**: SQLite file at `./studio.db`
- **Logs**: Check `./logs/` directory

---

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add feature"`
3. Push to GitHub: `git push origin feature/your-feature`
4. Open a Pull Request

GitHub Actions will automatically test your changes!

---

## 📄 License

This project is part of the MASSIVE DIGITAL suite.

---

## 📞 Support

- 🐛 **Bug Reports**: Open an issue on GitHub
- 💬 **Questions**: Check documentation or create a discussion
- 🚀 **Feature Requests**: Submit as an issue with `[FEATURE]` tag

---

## 🎵 System Status

- **Latest Build**: [![Build Status](https://github.com/digitalmassivegh/MASSIVE-RADIO-AUTOMATION-SYSTEM/actions/workflows/build.yml/badge.svg)](https://github.com/digitalmassivegh/MASSIVE-RADIO-AUTOMATION-SYSTEM/actions)
- **Python Support**: 3.9, 3.10, 3.11
- **Tested On**: Windows, macOS, Linux

---

**Made with ❤️ by MASSIVE DIGITAL**
