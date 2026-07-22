"""
PyInstaller spec file for MASSIVE RADIO AUTOMATION SYSTEM

Usage:
  pyinstaller main.spec

This creates a standalone executable that bundles:
- Python interpreter
- All dependencies (pygame, PyQt5, fastapi, etc.)
- All project files and assets
- Logo and UI resources

Output: dist/MASSIVE-RADIO/
"""

import os
import sys

# Get the directory where the spec file is located
datas = []
binaries = []
hiddenimports = [
    'pygame',
    'PyQt5',
    'PyQt5.QtWidgets',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'fastapi',
    'uvicorn',
    'uvicorn.logging',
    'pydub',
    'numpy',
    'sounddevice',
    'requests',
    'python_jose',
    'passlib',
    'jinja2',
]

# Include project directories and assets
datas += [
    ('ui/logo.png', 'ui'),
    ('db', 'db'),
    ('audio', 'audio'),
    ('sync', 'sync'),
    ('commercial', 'commercial'),
    ('ui', 'ui'),
    ('api', 'api'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MASSIVE-RADIO',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application (no console window)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='ui/logo.png',  # Windows taskbar icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MASSIVE-RADIO',
)
