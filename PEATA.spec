# -*- mode: python ; coding: utf-8 -*-

import platform
import os


# Platform-specific icon
if platform.system() == "Darwin":
    icon_file = "app/assets/peata_mac.icns"
else:
    icon_file = "app/assets/peata_win.ico"

# Platform-specific binaries or hidden imports (optional)

hiddenimports = []
datas=[
     ('app/assets/*', 'app/assets'),
     ('app/view/*', 'app/view'),
     ('app/controller/*', 'app/controller'),
     ('app/model/*', 'app/model'),
     (icon_file, 'app/assets'),
]

block_cipher = None

a = Analysis(
    ['./app/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide6'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    exclude_binaries=True,
    name='PEATA',
    icon=icon_file, # Dynamic icon path
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # True for debugging
    disable_windowed_traceback=False,
    argv_emulation=True, # Needed for .app drag/drop
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    windowed=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PEATA',
)
app = BUNDLE(
    coll,
    name='PEATA.app',
    icon=icon_file,
    bundle_identifier=None,
)
