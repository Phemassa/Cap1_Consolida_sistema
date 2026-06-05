@echo off
REM ============================================
REM Script de Restart do Servidor Flask
REM FarmTech Solutions - Sistema de Irrigação
REM ============================================

echo.
echo ========================================
echo   FarmTech Solutions - Restart Servidor
echo ========================================
echo.

echo [INFO] Procurando processos Python do Flask...

REM Mata todos os processos python.exe relacionados ao Flask
taskkill /F /IM python.exe /T 2>nul

if errorlevel 1 (
    echo [INFO] Nenhum servidor Flask em execução
) else (
    echo [INFO] Servidor Flask encerrado
    timeout /t 2 /nobreak >nul
)

echo [INFO] Iniciando novo servidor...
echo.

REM Chama o script de start
call "%~dp0start_server.bat"
