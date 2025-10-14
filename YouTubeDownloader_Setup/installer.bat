@echo off
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
set INSTALL_DIR=%ProgramFiles%\YouTubeDownloader
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copiar executável
copy /Y "YouTubeDownloader.exe" "%INSTALL_DIR%\YouTubeDownloader.exe" >nul

REM Criar atalho na área de trabalho
powershell "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\YouTube Downloader.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\YouTubeDownloader.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\YouTubeDownloader.exe'; $Shortcut.Description = 'Baixar vídeos do YouTube'; $Shortcut.Save()"

REM Criar atalho no Menu Iniciar
powershell "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\YouTube Downloader.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\YouTubeDownloader.exe'; $Shortcut.IconLocation = '%INSTALL_DIR%\YouTubeDownloader.exe'; $Shortcut.Description = 'Baixar vídeos do YouTube'; $Shortcut.Save()"

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
