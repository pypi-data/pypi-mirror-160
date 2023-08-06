# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('Data\\patchview.yaml', 'patchview\\Data'), ('Data\\icons\\*', 'patchview\\Data\icons'),
                    ('Data\\LICENSE.txt','patchview\\Data')],
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
          [],
          exclude_binaries=True,
          name='PatchView',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='Data\\icons\\PatchViewer.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='PatchView')
