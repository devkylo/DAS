import os
import subprocess
import sys
import shutil

def install_pyinstaller():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

def create_spec_file():
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('이미지', '이미지'),
        ('저장', '저장'),
        ('오디오', '오디오')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DAS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 콘솔 창이 출력되지 않도록 설정
    icon='DAS.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DAS',
    onefile=True,  # 한 파일로 묶기
)
"""
    with open('DAS.spec', 'w', encoding='utf-8') as spec_file:
        spec_file.write(spec_content)

def convert_png_to_ico(png_path, ico_path):
    from PIL import Image
    img = Image.open(png_path)
    img.save(ico_path, format='ICO', sizes=[(32, 32), (64, 64), (128, 128), (256, 256)])

def setup_internal_directory():
    dist_DAS_dir = os.path.join('dist', 'DAS')
    internal_dir = os.path.join(dist_DAS_dir, '_internal')
    
    if not os.path.exists(internal_dir):
        os.makedirs(internal_dir)
    
    if not os.path.isfile(os.path.join(internal_dir, 'DAS.png')):
        shutil.copy('DAS.png', os.path.join(internal_dir, 'DAS.png'))
    
    processed_storage_dir = os.path.join(internal_dir, '가공저장')
    if not os.path.exists(processed_storage_dir):
        os.makedirs(processed_storage_dir)

def run_pyinstaller():
    creationflags = subprocess.CREATE_NO_WINDOW  # CREATE_NO_WINDOW
    subprocess.check_call(['pyinstaller', 'DAS.spec'], creationflags=creationflags)
    
def main():
    # Check if PyInstaller is installed, if not, install it
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller가 설치되어 있지 않습니다. 설치 중...")
        install_pyinstaller()

    # Ensure main.py exists in the current directory
    if not os.path.isfile('main.py'):
        print("오류: 'main.py' 파일이 현재 디렉토리에 없습니다.")
        sys.exit(1)

    # Ensure DAS.png exists in the current directory
    if not os.path.isfile('DAS.png'):
        print("오류: 'DAS.png' 파일이 현재 디렉토리에 없습니다.")
        sys.exit(1)

    # Convert DAS.png to DAS.ico
    convert_png_to_ico('DAS.png', 'DAS.ico')

    # Create the spec file
    create_spec_file()

    # Run PyInstaller with the spec file
    run_pyinstaller()

    # Setup _internal directory within dist/DAS
    setup_internal_directory()

if __name__ == '__main__':
    main()
