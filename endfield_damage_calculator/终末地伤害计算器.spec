# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# 获取spec文件所在目录作为项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))

a = Analysis(
    [os.path.join(project_root, 'main.py')],
    pathex=[project_root],
    binaries=[],
    datas=[
        (os.path.join(project_root, 'character_weapon_equipment', 'character_data', 'characters.json'), 'character_weapon_equipment/character_data/'),
        (os.path.join(project_root, 'character_weapon_equipment', 'weapon_data', 'weapons.json'), 'character_weapon_equipment/weapon_data/')
    ],
    hiddenimports=[],
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
    name='终末地伤害计算器',
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
)
