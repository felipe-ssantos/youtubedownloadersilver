@echo off
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
set INSTALL_DIR=%ProgramFiles%\YouTubeDownloader
if exist "%INSTALL_DIR%" rmdir /S /Q "%INSTALL_DIR%"

REM Remover atalho da área de trabalho
del "%USERPROFILE%\Desktop\YouTube Downloader.lnk" 2>nul

REM Remover atalho do Menu Iniciar
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\YouTube Downloader.lnk" 2>nul

echo.
echo ========================================
echo   Desinstalacao concluida!
echo ========================================
echo.
pause
