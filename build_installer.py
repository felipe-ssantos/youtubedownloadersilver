# build_installer.py
# Execute este script para criar o instalador automático

import os
import subprocess
import sys
import glob

# Variável global para o arquivo principal
MAIN_FILE = None

def find_main_file():
    """Encontra o arquivo principal do programa"""
    possible_names = [
        'youtube_downloader.py',
        'baixar_youtube-v3-python.py',
        'baixar_youtube*.py'
    ]
    
    for pattern in possible_names:
        files = glob.glob(pattern)
        if files:
            return files[0]
    
    return None

def install_requirements():
    """Instala todas as dependências necessárias"""
    print("=" * 60)
    print("INSTALANDO DEPENDÊNCIAS PARA BUILD")
    print("=" * 60)
    
    packages = [
        'yt-dlp',
        'pyinstaller',
        'pillow'
    ]
    
    for package in packages:
        print(f"\n📦 Instalando {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except:
            print(f"⚠️ Aviso: {package} pode já estar instalado")
    
    print("\n✅ Todas as dependências foram instaladas!\n")

def create_icon():
    """Cria um ícone simples para o executável"""
    print("🎨 Criando ícone...")
    
    try:
        from PIL import Image, ImageDraw
        
        # Criar imagem 256x256
        img = Image.new('RGB', (256, 256), color='#0066cc')
        draw = ImageDraw.Draw(img)
        
        # Desenhar círculo branco
        draw.ellipse([30, 30, 226, 226], fill='white')
        
        # Desenhar seta de download (aproximação simples)
        draw.polygon([(128, 80), (128, 150), (90, 150), (128, 190), (166, 150), (128, 150)], fill='#0066cc')
        
        # Salvar como ICO
        img.save('icon.ico', format='ICO')
        print("✅ Ícone criado: icon.ico\n")
        return True
    except Exception as e:
        print(f"⚠️ Não foi possível criar ícone: {e}")
        print("   Continuando sem ícone customizado...\n")
        return False

def build_executable():
    """Cria o executável usando PyInstaller"""
    print("=" * 60)
    print("CRIANDO EXECUTÁVEL")
    print("=" * 60)
    
    global MAIN_FILE
    
    # Comando PyInstaller com todas as opções
    cmd = [
        'pyinstaller',
        '--onefile',                    # Arquivo único
        '--windowed',                   # Sem console
        '--name=YouTubeDownloader',     # Nome do executável
        '--clean',                      # Limpar build anterior
        '--hidden-import=yt_dlp',
        '--hidden-import=urllib3',
        '--hidden-import=certifi',
        '--collect-all=yt_dlp',
    ]
    
    # Adicionar ícone se existir
    if os.path.exists('icon.ico'):
        cmd.append('--icon=icon.ico')
    
    # Adicionar o arquivo principal
    cmd.append(MAIN_FILE)
    
    print(f"\n📄 Usando arquivo: {MAIN_FILE}")
    print(f"🔨 Executando PyInstaller...\n")
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Executável criado com sucesso!")
        print(f"📁 Localização: {os.path.abspath('dist/YouTubeDownloader.exe')}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao criar executável: {e}")
        print("\n💡 Dica: Certifique-se de que pyinstaller está instalado:")
        print("   pip install pyinstaller\n")
        return False

def create_installer_script():
    """Cria um script batch para instalação automática"""
    print("=" * 60)
    print("CRIANDO SCRIPT DE INSTALAÇÃO")
    print("=" * 60)
    
    installer_content = """@echo off
title YouTube Downloader - Instalador
color 0A
echo.
echo ========================================
echo   YouTube Downloader Pro - Instalador
echo ========================================
echo.
echo Instalando o programa...
echo.

REM Criar pasta do programa
set INSTALL_DIR=%ProgramFiles%\\YouTubeDownloader
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copiar executável
copy /Y "YouTubeDownloader.exe" "%INSTALL_DIR%\\YouTubeDownloader.exe" >nul

REM Criar atalho na área de trabalho
powershell "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\YouTube Downloader.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\YouTubeDownloader.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\\YouTubeDownloader.exe'; $Shortcut.Description = 'Baixar vídeos do YouTube'; $Shortcut.Save()"

REM Criar atalho no Menu Iniciar
powershell "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\YouTube Downloader.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\YouTubeDownloader.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\\YouTubeDownloader.exe'; $Shortcut.Description = 'Baixar vídeos do YouTube'; $Shortcut.Save()"

echo.
echo ========================================
echo   Instalacao concluida com sucesso!
echo ========================================
echo.
echo O programa foi instalado em:
echo %INSTALL_DIR%
echo.
echo Atalhos criados:
echo - Area de Trabalho
echo - Menu Iniciar
echo.
pause
"""
    
    with open('installer.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print("✅ Script de instalação criado: installer.bat\n")

def create_uninstaller():
    """Cria script de desinstalação"""
    print("🗑️ Criando desinstalador...")
    
    uninstaller_content = """@echo off
title YouTube Downloader - Desinstalador
color 0C
echo.
echo ========================================
echo   YouTube Downloader - Desinstalador
echo ========================================
echo.
echo Tem certeza que deseja desinstalar?
pause
echo.
echo Removendo programa...

REM Remover pasta do programa
set INSTALL_DIR=%ProgramFiles%\\YouTubeDownloader
if exist "%INSTALL_DIR%" rmdir /S /Q "%INSTALL_DIR%"

REM Remover atalho da área de trabalho
del "%USERPROFILE%\\Desktop\\YouTube Downloader.lnk" 2>nul

REM Remover atalho do Menu Iniciar
del "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\YouTube Downloader.lnk" 2>nul

echo.
echo ========================================
echo   Desinstalacao concluida!
echo ========================================
echo.
pause
"""
    
    with open('uninstaller.bat', 'w', encoding='utf-8') as f:
        f.write(uninstaller_content)
    
    print("✅ Desinstalador criado: uninstaller.bat\n")

def create_readme():
    """Cria arquivo README para distribuição"""
    print("📄 Criando README...")
    
    readme_content = """# YouTube Downloader Pro

## Instalação

1. Execute "installer.bat" como Administrador
2. Aguarde a conclusão da instalação
3. Use o atalho criado na Área de Trabalho

## Uso

1. Cole o link do vídeo do YouTube
2. Escolha o formato (MP4 ou MP3)
3. Selecione a qualidade desejada
4. Clique em "INICIAR DOWNLOAD"

## Desinstalação

Execute "uninstaller.bat" como Administrador

## Requisitos do Sistema

- Windows 10 ou superior
- Conexão com internet
- 100MB de espaço livre em disco

## Suporte

Para problemas ou dúvidas, visite:
https://github.com/yt-dlp/yt-dlp

## Licença

Este software é fornecido "como está", sem garantias.
"""
    
    with open('README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README criado: README.txt\n")

def create_distribution_package():
    """Cria pacote final de distribuição"""
    print("=" * 60)
    print("CRIANDO PACOTE DE DISTRIBUIÇÃO")
    print("=" * 60)
    
    # Criar pasta de distribuição
    dist_folder = 'YouTubeDownloader_Setup'
    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)
    
    # Copiar arquivos necessários
    files_to_copy = [
        ('dist/YouTubeDownloader.exe', f'{dist_folder}/YouTubeDownloader.exe'),
        ('installer.bat', f'{dist_folder}/installer.bat'),
        ('uninstaller.bat', f'{dist_folder}/uninstaller.bat'),
        ('README.txt', f'{dist_folder}/README.txt')
    ]
    
    print("\n📦 Copiando arquivos para o pacote...\n")
    
    import shutil
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"   ✓ {os.path.basename(dst)}")
        else:
            print(f"   ⚠️ {os.path.basename(src)} não encontrado")
    
    print(f"\n✅ Pacote criado em: {os.path.abspath(dist_folder)}")
    print("\n" + "=" * 60)
    print("PRONTO PARA DISTRIBUIÇÃO!")
    print("=" * 60)
    print(f"\n📁 Pasta: {dist_folder}")
    print("\nPara instalar:")
    print("1. Copie a pasta para o computador do usuário")
    print("2. Execute 'installer.bat' como Administrador")
    print("\n")

def main():
    global MAIN_FILE
    
    print("\n" + "=" * 60)
    print("   YOUTUBE DOWNLOADER - BUILD AUTOMÁTICO")
    print("=" * 60)
    print("\nEste script irá:")
    print("  1. Encontrar o arquivo principal do programa")
    print("  2. Instalar dependências necessárias")
    print("  3. Criar ícone do programa")
    print("  4. Compilar o executável")
    print("  5. Criar scripts de instalação/desinstalação")
    print("  6. Gerar pacote de distribuição")
    print("\n" + "=" * 60 + "\n")
    
    # Procurar arquivo principal
    print("🔍 Procurando arquivo principal...")
    MAIN_FILE = find_main_file()
    
    if not MAIN_FILE:
        print("❌ ERRO: Arquivo principal não encontrado!")
        print("\n   Procurei por:")
        print("   - youtube_downloader.py")
        print("   - baixar_youtube-v3-python.py")
        print("   - baixar_youtube*.py")
        print("\n   Execute este script na mesma pasta do programa.\n")
        input("Pressione ENTER para sair...")
        return
    
    print(f"✅ Arquivo encontrado: {MAIN_FILE}\n")
    
    input("Pressione ENTER para continuar...")
    print("\n")
    
    try:
        # Etapa 1: Instalar dependências
        install_requirements()
        
        # Etapa 2: Criar ícone
        create_icon()
        
        # Etapa 3: Criar executável
        if not build_executable():
            print("\n❌ Falha ao criar executável. Abortando...\n")
            input("Pressione ENTER para sair...")
            return
        
        # Etapa 4: Criar scripts de instalação
        create_installer_script()
        create_uninstaller()
        create_readme()
        
        # Etapa 5: Criar pacote de distribuição
        create_distribution_package()
        
        print("\n🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print("\nVocê pode agora distribuir a pasta 'YouTubeDownloader_Setup'")
        print("para qualquer usuário Windows!\n")
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE O BUILD: {e}\n")
        import traceback
        traceback.print_exc()
    
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()