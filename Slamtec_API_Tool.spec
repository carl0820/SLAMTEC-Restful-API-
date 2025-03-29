# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[('src', 'src')],
    hiddenimports=['PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'requests', 'python-dotenv', 'loguru', 'werkzeug', 'flask', 'sip', 'PyQt5.sip', 'json', 'os', 'sys', 'logging', 'threading', 'uuid'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=True,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('v', None, 'OPTION')],
    name='Slamtec_API_Tool',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
