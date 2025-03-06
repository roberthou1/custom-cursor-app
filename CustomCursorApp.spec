# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules

datas = [('README.md', '.')]
hiddenimports = []
datas += collect_data_files('PIL')
datas += collect_data_files('PyQt6.QtCore')
datas += collect_data_files('PyQt6.QtGui')
datas += collect_data_files('PyQt6.QtWidgets')
hiddenimports += collect_submodules('PIL')
hiddenimports += collect_submodules('PyQt6.QtCore')
hiddenimports += collect_submodules('PyQt6.QtGui')
hiddenimports += collect_submodules('PyQt6.QtWidgets')


a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[('venv/lib/python*/site-packages/PyQt6/Qt6/lib/QtCore.framework/Versions/A/QtCore', 'PyQt6/Qt6/lib/QtCore.framework/Versions/A/'), ('venv/lib/python*/site-packages/PyQt6/Qt6/lib/QtGui.framework/Versions/A/QtGui', 'PyQt6/Qt6/lib/QtGui.framework/Versions/A/'), ('venv/lib/python*/site-packages/PyQt6/Qt6/lib/QtWidgets.framework/Versions/A/QtWidgets', 'PyQt6/Qt6/lib/QtWidgets.framework/Versions/A/'), ('venv/lib/python*/site-packages/PyQt6/Qt6/plugins/platforms/libqcocoa.dylib', 'PyQt6/Qt6/plugins/platforms/'), ('venv/lib/python*/site-packages/PyQt6/Qt6/plugins/styles/libqmacstyle.dylib', 'PyQt6/Qt6/plugins/styles/')],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas', 'cryptography', 'PySide6', 'PyQt5', 'wx', 'PIL.ImageQt', 'PIL.ImageTk', 'PyQt6.QtNetwork', 'PyQt6.QtSql', 'PyQt6.QtMultimedia', 'PyQt6.QtQml', 'PyQt6.QtWebEngineCore', 'PyQt6.QtWebEngineWidgets', 'PyQt6.QtXml', 'email', 'html', 'http', 'logging', 'multiprocessing', 'unittest', 'xml', 'xmlrpc', 'pydoc'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CustomCursorApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icons/icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='CustomCursorApp',
)
app = BUNDLE(
    coll,
    name='CustomCursorApp.app',
    icon='icons/icon.icns',
    bundle_identifier='com.customcursor.app',
)
