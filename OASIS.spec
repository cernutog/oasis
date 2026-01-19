# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_all

# Dynamic paths for Tcl/Tk - uses Python's base prefix
PYTHON_HOME = sys.base_prefix
TCL_ROOT = os.path.join(PYTHON_HOME, "tcl")
DLLS_ROOT = os.path.join(PYTHON_HOME, "DLLs")
TKINTER_LIB = os.path.join(PYTHON_HOME, "Lib", "tkinter")

datas = [
    ('src/resources/redoc.standalone.js', 'src/resources'),
    ('src/colorschemes', 'src/colorschemes'),  # Custom color schemes
    ('src', 'src'),  # Include entire src directory to ensure all modules are available
    ('icon.ico', '.'),
    (os.path.join(TCL_ROOT, "tcl8.6"), "tcl/tcl8.6"),
    (os.path.join(TCL_ROOT, "tk8.6"), "tcl/tk8.6"),
    ('src/bin/spectral.exe', 'src/bin'),
    ('Templates Master', 'Templates Master'), # Bundle Templates
    # Explicitly include tkinter Python module
    (TKINTER_LIB, "tkinter"),
]
binaries = [
    (os.path.join(DLLS_ROOT, "tcl86t.dll"), "."),
    (os.path.join(DLLS_ROOT, "tk86t.dll"), "."),
    (os.path.join(DLLS_ROOT, "_tkinter.pyd"), ".")
]
hiddenimports = [
    'tkinter', 
    'src', 'src.gui', 'src.main', 'src.redoc_gen', 'src.linter', 'src.charts', 
    'src.preferences', 'src.preferences_dialog', 'src.doc_viewer', 'src.generator', 'src.excel_parser',
    'src.splash_screen',  # OASIS splash screen
    'webview', 'chlorophyll', 'pygments', 'pygments.lexers', 'tklinenums', 'tkinterweb', 
    'pygetwindow', 'pyrect',
    'PIL', 'PIL.Image', 'PIL.ImageTk',  # Pillow for splash screen images
]
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
# Chlorophyll colorschemes
tmp_ret = collect_all('chlorophyll')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
# tkinterweb for embedded HTML viewer
tmp_ret = collect_all('tkinterweb')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
# Tkinter - ensure all Python files are included
tmp_ret = collect_all('tkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

a = Analysis(
    ['run_gui.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['rthook_tcl.py'],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='OASIS',
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
    icon=['icon.ico'],
)
