@echo off
REM ============================================
REM Script de Inicialização do Servidor Flask
REM FarmTech Solutions - Sistema de Irrigação
REM ============================================

echo.
echo ========================================
echo   FarmTech Solutions - Servidor Flask
echo ========================================
echo.

REM Define o diretório do projeto
set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

REM Verifica se o ambiente virtual existe
if not exist ".venv\Scripts\python.exe" (
    echo [ERRO] Ambiente virtual não encontrado!
    echo Por favor, crie o ambiente virtual primeiro:
    echo    python -m venv .venv
    echo    .venv\Scripts\pip install flask requests
    pause
    exit /b 1
)

echo [INFO] Ambiente virtual encontrado
echo [INFO] Verificando dependências...

REM Ativa o ambiente virtual e verifica Flask
".venv\Scripts\python.exe" -c "import flask" 2>nul
if errorlevel 1 (
    echo [AVISO] Flask não instalado. Instalando...
    ".venv\Scripts\pip.exe" install flask requests
)

echo [INFO] Iniciando servidor Flask...
echo [INFO] Servidor disponível em:
echo        - Local: http://127.0.0.1:5000
echo        - Dashboard: http://127.0.0.1:5000
echo        - Meteorologia: http://127.0.0.1:5000/weather
echo.
echo [INFO] Pressione Ctrl+C para parar o servidor
echo ========================================
echo.

REM Inicia o servidor Flask
cd fase2\web_app
"%PROJECT_DIR%.venv\Scripts\python.exe" app.py

REM Se o servidor for interrompido
echo.
echo [INFO] Servidor encerrado.
pause
