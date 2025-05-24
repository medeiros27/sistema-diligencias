@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Sistema de Diligencias - Deploy v2.0
echo ========================================

rem 1) Ir para a raiz do projeto (parent folder de scripts)
cd /d "%~dp0\.."

echo.
echo 1. Verificando Python...
call python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Python nao encontrado!
    echo Baixe em: https://python.org
    pause
    goto :error
)

echo.
echo 2. Instalando dependencias...
call python "scripts\install_dependencies.py"
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Falha na instalacao de dependencias!
    pause
    goto :error
)

echo.
echo 3. Executando testes...
call python "tests\test_deploy.py"
if %ERRORLEVEL% NEQ 0 (
    echo AVISO: Alguns testes falharam
    rem continua mesmo com falhas de teste
)

echo.
echo 4. Construindo executavel...
call python "scripts\build.py"
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Falha no build!
    pause
    goto :error
)

echo.
echo 5. Criando atalho na area de trabalho...
set "DESKTOP=%USERPROFILE%\Desktop"
set "TARGET=%~dp0dist\SistemaDiligencias.exe"
set "SHORTCUT=%DESKTOP%\Sistema de Diligencias.lnk"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$WshShell = New-Object -ComObject WScript.Shell; ^
   $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); ^
   $Shortcut.TargetPath = '%TARGET%'; ^
   $Shortcut.Save()"

echo.
echo ========================================
echo          DEPLOY CONCLUIDO!
echo ========================================
echo.
echo Executavel: "dist\SistemaDiligencias.exe"
echo Atalho criado na area de trabalho
echo.
pause
exit /b 0

:error
echo.
echo DEPLOY ABORTADO!
exit /b 1