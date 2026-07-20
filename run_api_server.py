"""
run_api_server.py
-----------------
Entry point for the Radio Studio web API server.

Run this on your VPS (or locally for testing) — it is completely
independent of the desktop app.  The desktop connects TO this server;
you do not need to run both on the same machine.

Usage
-----
    # Development (auto-reload on file changes):
    python run_api_server.py

    # Production (Linux, behind nginx):
    uvicorn api_server.main:app --host 0.0.0.0 --port 8000 --workers 2

Environment variables
---------------------
    RADIO_SECRET_KEY   JWT signing secret (use a long random string in prod)
    RADIO_SERVER_DB    Path to the server SQLite file (default: data/server.db)
    PORT               Override the default port (useful for cloud platforms)

First-time setup
----------------
    1. Start the server:   python run_api_server.py
    2. Open the Swagger UI: http://localhost:8000/docs
    3. Register the first user via POST /auth/register
       (the first account created is automatically given the admin role)
    4. Log in via POST /auth/login to get a JWT token
    5. Copy the token into the desktop app's ⚙ Cloud Settings dialog
"""

import sys
import os

# Ensure api_server package is importable from this directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

from api_server.main import app   # noqa: F401  (import triggers startup hook)

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))

    print("=" * 60)
    print("  MASSIVE RADIO AUTOMATION SYSTEM — API Server")
    print("=" * 60)
    print(f"  Listening on : http://{host}:{port}")
    print(f"  Swagger UI   : http://localhost:{port}/docs")
    print(f"  ReDoc UI     : http://localhost:{port}/redoc")
    print("=" * 60)

    uvicorn.run(
        "api_server.main:app",
        host=host,
        port=port,
        reload=True,          # auto-reload on code changes (dev only)
        log_level="info",
    )
