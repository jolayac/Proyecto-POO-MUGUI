# -*- mode: python ; coding: utf-8 -*-
"""
Especificación de PyInstaller optimizada para MUGUI
Excluye librerías innecesarias para reducir tamaño del ejecutable
"""

a = Analysis(
    ['definitivo.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('imagenes', 'imagenes'),
        ('sonidos', 'sonidos'),
    ],
    hiddenimports=[
        'tkinter',
        'pygame',
        'librosa',
        'pyaudio',
        'numpy',
        'mutagen',
        'firebase_admin',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[
        'matplotlib',
        'scipy',
        'pytest',
        'setuptools',
        'wheel',
        'distutils',
        'pkg_resources',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MUGUI',
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
    icon='imagenes/icono.ico',
)
