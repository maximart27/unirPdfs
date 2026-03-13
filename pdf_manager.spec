# pdf_manager.spec
# Compilar con:  pyinstaller pdf_manager.spec

from PyInstaller.utils.hooks import collect_all

pymupdf_datas, pymupdf_binaries, pymupdf_hiddenimports = collect_all('pymupdf')

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=pymupdf_binaries,
    datas=[
        ('ui',      'ui'),
        ('core',    'core'),
        ('PDF.ico', '.'),
        *pymupdf_datas,
    ],
    hiddenimports=[
        'pymupdf',
        'pymupdf.fitz',
        *pymupdf_hiddenimports,
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pdf-manager',
    debug=False,
    strip=False,
    upx=True,
    console=False,   # sin ventana de terminal
    icon='PDF.ico',
)
