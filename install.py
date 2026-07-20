"""
MASSIVE RADIO AUTOMATION SYSTEM
Master installer — works on Windows, macOS, and Linux.

Run once:
    python install.py      (or double-click INSTALL.bat / INSTALL.command)

What it does:
  1. Checks Python version (3.8+ required)
  2. Creates a self-contained virtual environment inside this folder  (venv/)
  3. Installs all Python dependencies into that venv
  4. Installs PortAudio system library on Linux/macOS (needed for mic input)
  5. Creates the first-run data directories and blank database
  6. Prints how to start the application
"""

import sys, os, subprocess, platform, shutil
from pathlib import Path

APP_NAME  = "MASSIVE RADIO AUTOMATION SYSTEM"
APP_SHORT = "MassiveRadio"
VENV_DIR  = Path(__file__).parent / "venv"
ROOT      = Path(__file__).parent
REQ_FILE  = ROOT / "requirements.txt"

# ── helpers ───────────────────────────────────────────────────────────────────

def banner(text):
    w = max(len(text) + 4, 56)
    print("\n" + "═" * w)
    print(f"  {text}")
    print("═" * w)

def step(text):
    print(f"\n  ▶  {text}")

def ok(text):
    print(f"  ✔  {text}")

def warn(text):
    print(f"  ⚠  {text}")

def err(text):
    print(f"\n  ✘  ERROR: {text}\n")

def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, **kwargs)

# ── system audio library (PortAudio) ─────────────────────────────────────────

def install_portaudio():
    system = platform.system()
    if system == "Linux":
        step("Installing PortAudio (system audio library)...")
        if shutil.which("apt-get"):
            run(["sudo", "apt-get", "install", "-y",
                 "libportaudio2", "portaudio19-dev",
                 "libportaudio2", "ffmpeg"], capture_output=False)
        elif shutil.which("dnf"):
            run(["sudo", "dnf", "install", "-y", "portaudio-devel", "ffmpeg"])
        elif shutil.which("pacman"):
            run(["sudo", "pacman", "-S", "--noconfirm", "portaudio", "ffmpeg"])
        else:
            warn("Could not detect package manager. Install 'portaudio' manually if mic input fails.")
    elif system == "Darwin":
        if shutil.which("brew"):
            step("Installing PortAudio via Homebrew...")
            run(["brew", "install", "portaudio", "ffmpeg"], capture_output=False)
        else:
            warn("Homebrew not found. If mic input fails, install it from https://brew.sh then run:  brew install portaudio")
    # Windows: sounddevice bundles its own PortAudio DLL — nothing to do

# ── virtual environment ───────────────────────────────────────────────────────

def create_venv():
    step(f"Creating virtual environment at  venv/")
    run([sys.executable, "-m", "venv", str(VENV_DIR)])
    ok("Virtual environment created")

def venv_python():
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"

def venv_pip():
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "pip.exe"
    return VENV_DIR / "bin" / "pip"

def install_deps():
    step("Installing Python dependencies (this may take a few minutes)...")
    pip = str(venv_pip())

    # Always upgrade pip first — old pip often fails on newer packages
    run([pip, "install", "--upgrade", "pip", "setuptools", "wheel", "--quiet"])

    # ── Essential packages (must succeed) ────────────────────────────────────
    essential = [
        "PyQt5>=5.15.0",
        "pygame>=2.1.0",
        "requests>=2.31.0",
        "fastapi>=0.111.0",
        "uvicorn[standard]>=0.29.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.9",
        "aiofiles>=23.0.0",
        "jinja2>=3.1.0",
    ]

    # ── Optional packages (app works without them if they fail) ──────────────
    optional = {
        "pydub>=0.25.1":     "Audio silence detection (non-critical)",
        "numpy>=1.24.0":     "Numeric processing (non-critical)",
        "sounddevice>=0.4.6":"Live microphone input (non-critical)",
    }

    # Install essential packages one-by-one for clear error messages
    failed = []
    for pkg in essential:
        print(f"    Installing {pkg.split('>=')[0].split('[')[0]}...")
        try:
            run([pip, "install", pkg, "--quiet"])
        except subprocess.CalledProcessError:
            failed.append(pkg)
            warn(f"Failed to install {pkg}")

    if failed:
        err("The following essential packages could not be installed:")
        for f in failed:
            print(f"      {f}")
        print()
        print("  Common fixes:")
        print("  • Run INSTALL.bat as Administrator (right-click → Run as administrator)")
        print("  • Check your internet connection and try again")
        sys.exit(1)

    # Install optional packages — skip and warn if they fail
    skipped = []
    for pkg, desc in optional.items():
        name = pkg.split('>=')[0]
        print(f"    Installing {name}...")
        try:
            run([pip, "install", pkg, "--quiet"])
        except subprocess.CalledProcessError:
            warn(f"Skipped {name} ({desc})")
            skipped.append(name)

    if skipped:
        print()
        warn(f"Optional features skipped (app will still work): {', '.join(skipped)}")

    ok("Dependencies installed")

# ── first-run data directories ────────────────────────────────────────────────

def create_dirs():
    step("Creating application data directories...")
    for d in ["data", "media", "logs", "exports"]:
        (ROOT / d).mkdir(exist_ok=True)
    ok("Directories ready: data/  media/  logs/  exports/")

def bootstrap_db():
    """Create blank studio.db with all required tables."""
    db_path = ROOT / "data" / "studio.db"
    if db_path.exists():
        ok("Database already exists — skipping")
        return
    step("Creating blank database...")
    import sqlite3
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT DEFAULT '',
        duration_sec REAL DEFAULT 0,
        local_path TEXT,
        remote_id TEXT,
        category TEXT DEFAULT 'music',
        last_played TEXT,
        play_count INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT DEFAULT '',
        category TEXT DEFAULT 'news',
        priority INTEGER DEFAULT 0,
        status TEXT DEFAULT 'draft',
        remote_id TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id INTEGER,
        position INTEGER DEFAULT 0,
        scheduled_time TEXT,
        played INTEGER DEFAULT 0,
        played_at TEXT,
        FOREIGN KEY (track_id) REFERENCES tracks(id)
    );
    CREATE TABLE IF NOT EXISTS jingle_assignments (
        button_index INTEGER PRIMARY KEY,
        track_id INTEGER,
        label TEXT,
        FOREIGN KEY (track_id) REFERENCES tracks(id)
    );
    CREATE TABLE IF NOT EXISTS hour_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hour INTEGER,
        segment_type TEXT,
        duration_sec REAL,
        notes TEXT
    );
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        client TEXT DEFAULT '',
        spots_per_hour INTEGER DEFAULT 1,
        active INTEGER DEFAULT 1,
        start_date TEXT,
        end_date TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS asrun_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_id INTEGER,
        campaign_id INTEGER,
        played_at TEXT DEFAULT CURRENT_TIMESTAMP,
        deck TEXT DEFAULT 'A',
        duration_sec REAL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS sync_meta (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """
    cur.executescript(sql)
    con.commit()
    con.close()
    ok(f"Database created: data/studio.db")

# ── main ──────────────────────────────────────────────────────────────────────

def main(silent: bool = False):
    banner(f"Installing  {APP_NAME}")

    # Python version check
    if sys.version_info < (3, 8):
        err(f"Python 3.8 or newer is required. You have {sys.version}.")
        err("Download Python from  https://www.python.org/downloads/")
        sys.exit(1)
    ok(f"Python {sys.version.split()[0]}  ✓")

    # System audio library
    install_portaudio()

    # Virtual environment
    if VENV_DIR.exists():
        warn("venv/ already exists — upgrading dependencies")
    else:
        create_venv()

    # Python packages
    install_deps()

    # Data directories + database
    create_dirs()
    bootstrap_db()

    # Done
    system = platform.system()
    if system == "Windows":
        start_cmd = "START.bat  (double-click)"
    elif system == "Darwin":
        start_cmd = "START.command  (double-click)"
    else:
        start_cmd = "bash start.sh"

    banner("Installation complete!")
    print(f"""
  To launch {APP_SHORT}:

      {start_cmd}

  The app stores all data inside this folder:
      data/      — local database
      media/     — audio files
      logs/      — as-run logs

  Nothing is written outside this folder.
  To uninstall: delete this entire folder.
""")


if __name__ == "__main__":
    silent = "--silent" in sys.argv
    try:
        main(silent=silent)
    except KeyboardInterrupt:
        print("\n\n  Installation cancelled.\n")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        err(f"A setup command failed: {e}")
        print("  Check the output above for details.\n")
        sys.exit(1)
    finally:
        if not silent:
            input("  Press Enter to close this window...")
