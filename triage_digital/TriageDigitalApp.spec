# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['app_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('apps', 'apps'),
        ('config', 'config'),
        ('manage.py', '.'),
        ('requirements.txt', '.'),
        ('db', 'db'),
    ],
    hiddenimports=[
        'django',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'apps.triage',
        'apps.patients',
        'reportlab.pdfgen.canvas',
        'reportlab.lib.pagesizes',
    ],
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
    a.binaries,
    a.datas,
    [],
    name='TriageDigital',
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
    icon='triage_icon.ico',
)
