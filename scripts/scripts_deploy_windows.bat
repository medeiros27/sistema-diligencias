@echo off
echo ========================================
echo  Sistema de Diligencias - Deploy v2.0
echo ========================================

echo.
echo 1. Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Baixe em: https://python.org
    pause
    exit /b 1
)

echo.
echo 2. Instalando dependencias...
python scripts/install_dependencies.py
if errorlevel 1 (
    echo ERRO: Falha na instalacao de dependencias!
    pause
    exit /b 1
)

echo.
echo 3. Executando testes...
python tests/test_deploy.py
if errorlevel 1 (
    echo AVISO: Alguns testes falharam
)

echo.
echo 4. Construindo executavel...
python scripts/build.py
if errorlevel 1 (
    echo ERRO: Falha no build!
    pause
    exit /b 1
)

echo.
echo 5. Criando atalho na area de trabalho...
set DESKTOP=%USERPROFILE%\Desktop
set TARGET=%~dp0dist\SistemaDiligencias.exe
set SHORTCUT=%DESKTOP%\Sistema de Diligencias.lnk

powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%TARGET%'; $Shortcut.Save()"

echo.
echo ========================================
echo          DEPLOY CONCLUIDO!
echo ========================================
echo.
echo Executavel: dist\SistemaDiligencias.exe
echo Atalho criado na area de trabalho
echo.
pause