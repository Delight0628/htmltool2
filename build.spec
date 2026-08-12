# -*- mode: python ; coding: utf-8 -*-
"""
页琢 PyInstaller 打包配置
使用方法: pyinstaller build.spec
产出: dist/页琢.exe
"""
import os

BLOCK_cipher = None
BASE_DIR = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    [os.path.join(BASE_DIR, "tray_server.py")],
    pathex=[BASE_DIR],
    binaries=[],
    datas=[
        (os.path.join(BASE_DIR, "icon.png"), "."),
        (os.path.join(BASE_DIR, "icon.ico"), "."),
        (os.path.join(BASE_DIR, "index.html"), "."),
        (os.path.join(BASE_DIR, "test.html"), "."),
    ],
    hiddenimports=[
        "pystray._win32",
        "PIL",
        "PIL._tkinter_finder",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=BLOCK_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=BLOCK_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="页琢",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(BASE_DIR, "icon.ico"),
)
