# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all

datas = [('README.md', '.'), ('src/custom_cursor_app', 'custom_cursor_app')]
binaries = [('venv/lib/python*/site-packages/PyQt6/Qt6/plugins/platforms/libqcocoa.dylib', 'PyQt6/Qt6/plugins/platforms/'), ('venv/lib/python*/site-packages/PyQt6/Qt6/plugins/styles/libqmacstyle.dylib', 'PyQt6/Qt6/plugins/styles/')]
hiddenimports = ['custom_cursor_app', 'custom_cursor_app.app', 'struct', '_struct', 'importlib', 'importlib.util', 'logging', 'glob']
datas += collect_data_files('PIL')
datas += collect_data_files('PyQt6.QtCore')
datas += collect_data_files('PyQt6.QtGui')
datas += collect_data_files('PyQt6.QtWidgets')
hiddenimports += collect_submodules('PIL')
hiddenimports += collect_submodules('PyQt6.QtCore')
hiddenimports += collect_submodules('PyQt6.QtGui')
hiddenimports += collect_submodules('PyQt6.QtWidgets')
tmp_ret = collect_all('PyQt6.QtCore')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PyQt6.QtGui')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PyQt6.QtWidgets')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas', 'cryptography', 'PySide6', 'PyQt5', 'wx', 'PIL.ImageQt', 'PIL.ImageTk', 'PyQt6.QtNetwork', 'PyQt6.QtSql', 'PyQt6.QtMultimedia', 'PyQt6.QtQml', 'PyQt6.QtWebEngineCore', 'PyQt6.QtWebEngineWidgets', 'PyQt6.QtXml', 'email', 'html', 'http', 'logging', 'multiprocessing', 'unittest', 'xml', 'xmlrpc', 'pydoc'],
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
    name='Custom Cursors',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons/icon.icns'],
)
app = BUNDLE(
    exe,
    name='Custom Cursors.app',
    icon='icons/icon.icns',
    bundle_identifier='com.customcursor.app',
)
