# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all

datas = [('/Users/artem/Documents/Pulsarify/data', './data'), ('/Users/artem/Documents/Pulsarify/src', './src')]
binaries = []
hiddenimports = ['PIL', 'PIL.Image', 'PIL.ImageDraw', 'PIL.ImageFont', 'PIL._imaging', 'PIL._imagingcms']
hiddenimports += collect_submodules('Pillow')
tmp_ret = collect_all('Pillow')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Pulsarify',
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
    name='Pulsarify',
)
app = BUNDLE(
    coll,
    name='Pulsarify.app',
    icon=None,
    bundle_identifier=None,
)
