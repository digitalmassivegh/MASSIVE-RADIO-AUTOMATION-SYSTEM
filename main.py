"""
main.py
-------
Desktop application entry point — Phase 2.

Startup sequence
----------------
1. Initialise config (config.json auto-created on first run).
2. Initialise the local SQLite database (schema created if absent).
3. Initialise pygame audio mixer.
4. Start the Qt application.
5. Create the AudioEngine.
6. Create and start the SyncEngine (daemon thread).
7. Open the MainWindow.

Run with:
    python main.py

The web API server is a completely separate process:
    python run_api_server.py
"""

import sys
import os

# ── Make sub-packages importable ────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Suppress pygame banner
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore    import Qt, QTimer
from PyQt5.QtGui     import QFont, QIcon, QPixmap, QPainter, QColor, QPen

# Import config first — creates config.json and directories
from config import cfg

# Import local DB — creates studio.db and schema
from db.local_db import db as local_db

from audio.player            import AudioEngine
from audio.processor         import AudioProcessor
from audio.auto_player       import AutoPlayer
from audio.mic_engine        import MicEngine
from sync.sync_engine        import SyncEngine
from commercial.scheduler    import CommercialScheduler
from commercial.asrun_logger import AsRunLogger
from ui.main_window          import MainWindow
from ui.styles               import GLOBAL_STYLE

_APP_DIR = os.path.dirname(os.path.abspath(__file__))
_LOGO    = os.path.join(_APP_DIR, "ui", "logo.png")


def _make_splash(logo_path: str) -> QSplashScreen:
    """Build a branded splash screen (600×400) from the logo PNG."""
    base = QPixmap(600, 400)
    base.fill(QColor("#121212"))

    splash = QSplashScreen(base, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)

    # Paint logo centred on the dark background
    pm = QPixmap(logo_path)
    if not pm.isNull():
        scaled = pm.scaled(340, 240, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        p = QPainter(base)
        x = (600 - scaled.width())  // 2
        y = (400 - scaled.height()) // 2 - 20
        p.drawPixmap(x, y, scaled)

        # Waveform accent line
        pen = QPen(QColor("#FF2D55"), 2)
        p.setPen(pen)
        p.drawLine(60, 360, 540, 360)

        # Version / loading text
        p.setPen(QColor("#888888"))
        p.setFont(QFont("Segoe UI", 9))
        p.drawText(0, 375, 600, 20, Qt.AlignCenter,
                   "MASSIVE RADIO AUTOMATION SYSTEM  —  Loading…")
        p.end()
        splash.setPixmap(base)

    return splash


def main():
    # ── 1. Pygame audio pre-init ────────────────────────────────────────────
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=2048)
    pygame.init()

    # ── 2. Qt application ───────────────────────────────────────────────────
    app = QApplication(sys.argv)
    app.setApplicationName("Massive Radio Automation System")
    app.setOrganizationName("MassiveRadio")

    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps,    True)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(GLOBAL_STYLE)

    # App-wide taskbar / dock icon
    if os.path.exists(_LOGO):
        app.setWindowIcon(QIcon(_LOGO))

    # Splash screen (shown while engines initialise)
    splash = None
    if os.path.exists(_LOGO):
        splash = _make_splash(_LOGO)
        splash.show()
        app.processEvents()

    # ── 3. Audio engine ─────────────────────────────────────────────────────
    audio_engine = AudioEngine()

    # ── 3b. Microphone engine (live talkover + auto-ducking) ─────────────────
    mic_engine = MicEngine(audio_engine=audio_engine)

    # ── 4. Audio processor (silence detection + normalisation) ──────────────
    processor = AudioProcessor()

    # ── 5. Auto-player (dual-deck queue management) ──────────────────────────
    auto_player = AutoPlayer(
        audio_engine=audio_engine,
        local_db=local_db,
        processor=processor,
    )

    # ── 6. As-Run compliance logger ─────────────────────────────────────────
    logs_dir    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    asrun_logger = AsRunLogger(local_db=local_db, log_dir=logs_dir)

    # Wire AutoPlayer commercial signals → AsRunLogger
    auto_player.commercial_ended.connect(
        lambda info: asrun_logger.log_play(
            advertiser=info.get("advertiser", ""),
            filename=info.get("filename", ""),
            track_id=info.get("track_id", 0),
            status=info.get("status", "Played Fully"),
        )
    )

    # ── 7. Commercial scheduler ──────────────────────────────────────────────
    commercial_scheduler = CommercialScheduler(local_db=local_db)
    commercial_scheduler.break_due.connect(auto_player.inject_commercial_break)
    commercial_scheduler.start()

    # ── 8. Sync engine ──────────────────────────────────────────────────────
    sync_engine = SyncEngine(local_db=local_db)
    sync_engine.start()   # starts background daemon thread immediately

    # ── 9. Main window ──────────────────────────────────────────────────────
    window = MainWindow(
        audio_engine=audio_engine,
        sync_engine=sync_engine,
        auto_player=auto_player,
        commercial_scheduler=commercial_scheduler,
        mic_engine=mic_engine,
    )
    window.show()

    # Close splash once main window is visible
    if splash:
        splash.finish(window)

    print("[MASSIVE RADIO] System ready.")
    print(f"[MASSIVE RADIO] Local database  : {cfg.db_path}")
    print(f"[MASSIVE RADIO] Media folder    : {cfg.media_folder}")
    print(f"[MASSIVE RADIO] As-run logs     : {logs_dir}")
    print(f"[MASSIVE RADIO] API server URL  : {cfg.api_url}")
    print(f"[MASSIVE RADIO] Sync enabled    : {cfg.sync_enabled}")
    print(f"[MASSIVE RADIO] Microphone      : {'Available' if mic_engine.available else 'Unavailable (no PortAudio)'}")
    if not cfg.sync_enabled:
        print("[MASSIVE RADIO] To enable sync: click ⚙ Cloud Settings in the app.")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
