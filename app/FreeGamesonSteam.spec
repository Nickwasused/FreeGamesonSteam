# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['steam.py'],
             pathex=['C:\\Users\\Nick\\OneDrive\\Dokumente\\GitHub\\FreeGamesonSteam\\app'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='FreeGamesonStean',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

import shutil
shutil.copyfile('steamconfig.py', '{0}/steamconfig.py'.format(DISTPATH))
