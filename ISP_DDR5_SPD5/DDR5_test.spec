# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['DDR5_test.py'],
             pathex=[],
             binaries=[('C:\Windows\System32\libusb-1.0.dll', '.'),( 'Gang_USB_Lib.dll', '.' ),],
             datas=[('./image/NuTool.ico', '.'),
                    ('./image/320px-Nuvoton.png', '.'),
                    ('./image/Nuvoton.png', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='DDR5_test',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='./image/exe.ico',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
