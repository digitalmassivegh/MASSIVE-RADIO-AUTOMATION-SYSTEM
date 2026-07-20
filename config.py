"""
config.py
---------
Central configuration for the Radio Studio desktop app.

All tuneable values live here so Phase 3 can add a Settings UI
that writes to config.json without touching any other source file.

On first run, config.json is created automatically with these defaults.
"""

import os
import json

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

# ── Default values (written to config.json on first run) ─────────────────────
DEFAULTS = {
    # Local data
    "db_path":      os.path.join(BASE_DIR, "data", "studio.db"),
    "media_folder": os.path.join(BASE_DIR, "media"),

    # Web API
    "api_url":      "http://localhost:8000",   # change to VPS URL for production
    "api_token":    "",                         # filled in after first login

    # Sync engine
    "sync_interval_seconds": 300,              # 5 minutes
    "sync_enabled":          False,            # off until API URL is configured

    # Audio
    "crossfade_duration": 5.0,

    # Microphone / ducking  (Phase 5)
    "mic_device_index":  None,   # None = system default input
    "mic_duck_level":    0.15,   # music volume while MIC ON (0–1.0)
    "mic_duck_ramp_ms":  300,    # ms to duck down on MIC ON
    "mic_unduck_ramp_ms": 600,   # ms to restore volume on MIC OFF
}


class Config:
    """
    Singleton configuration object.

    Usage (anywhere in the app):
        from config import cfg
        url = cfg.api_url
        cfg.set("api_token", "abc123")   # persists to disk
    """

    def __init__(self):
        self._data: dict = {}
        self._load()

    # ── Load / save ──────────────────────────────────────────────────────────

    def _load(self):
        """Load config.json; fill in any missing keys from DEFAULTS."""
        if os.path.isfile(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as fh:
                    self._data = json.load(fh)
            except (json.JSONDecodeError, OSError):
                self._data = {}
        # Merge defaults for any missing keys
        changed = False
        for key, val in DEFAULTS.items():
            if key not in self._data:
                self._data[key] = val
                changed = True
        if changed:
            self._save()

        # Ensure media folder exists
        os.makedirs(self._data["media_folder"], exist_ok=True)
        # Ensure local db directory exists
        os.makedirs(os.path.dirname(self._data["db_path"]), exist_ok=True)

    def _save(self):
        """Persist current config to disk."""
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as fh:
                json.dump(self._data, fh, indent=2)
        except OSError as exc:
            print(f"[Config] Could not save config.json: {exc}")

    # ── Attribute-style access ────────────────────────────────────────────────

    def __getattr__(self, key: str):
        if key.startswith("_"):
            raise AttributeError(key)
        try:
            return self._data[key]
        except KeyError:
            raise AttributeError(f"Config has no key '{key}'")

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        """Update a single key and immediately persist to disk."""
        self._data[key] = value
        self._save()


# ── Module-level singleton ────────────────────────────────────────────────────
cfg = Config()
