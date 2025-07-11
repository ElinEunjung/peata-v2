# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules

hiddenimports=[
    'PyQt5.sip',
    'PyQt5.QtCore', 
    'PyQt5.QtGui', 
    'PyQt5.QtWidgets',
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebEngineCore'
] + collect_submodules('PyQt5.QtWebEngineWidgets') + collect_submodules('PyQt5.QtWebEngineCore')

datas=[
     ('app/assets/*', 'app/assets'),
     ('app/view/*', 'app/view'),
     ('app/controller/*', 'app/controller'),
     ('app/model/*', 'app/model'),
     ('D:/Programs/Anaconda3/Library/bin/QtWebEngineProcess.exe', 'PyQt5/Qt5/bin'),
     ('D:/Programs/Anaconda3/Library/qml/QtWebEngine', 'PyQt5/Qt5/qml/QtWebEngine'),
]

a = Analysis(
    ['app\\main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PySide6'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PEATA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PEATA',
)
