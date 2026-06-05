# ============================================
# Script PowerShell - Inicialização Servidor Flask
# FarmTech Solutions - Sistema de Irrigação
# ============================================

Write-Host ""
Write-Host "========================================"
Write-Host "  FarmTech Solutions - Servidor Flask"
Write-Host "========================================"
Write-Host ""

# Define o diretório do projeto
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir

# Verifica se o ambiente virtual existe
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[ERRO] Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, crie o ambiente virtual primeiro:" -ForegroundColor Yellow
    Write-Host "   python -m venv .venv" -ForegroundColor Cyan
    Write-Host "   .venv\Scripts\pip install flask requests" -ForegroundColor Cyan
    pause
    exit 1
}

Write-Host "[INFO] Ambiente virtual encontrado" -ForegroundColor Green
Write-Host "[INFO] Verificando dependências..." -ForegroundColor Cyan

# Verifica se Flask está instalado
try {
    & "$ProjectDir\.venv\Scripts\python.exe" -c "import flask" 2>$null
} catch {
    Write-Host "[AVISO] Flask não instalado. Instalando..." -ForegroundColor Yellow
    & "$ProjectDir\.venv\Scripts\pip.exe" install flask requests
}

Write-Host ""
Write-Host "[INFO] Iniciando servidor Flask..." -ForegroundColor Green
Write-Host "[INFO] Servidor disponível em:" -ForegroundColor Cyan
Write-Host "       - Local: http://127.0.0.1:5000" -ForegroundColor White
Write-Host "       - Dashboard: http://127.0.0.1:5000" -ForegroundColor White
Write-Host "       - Meteorologia: http://127.0.0.1:5000/weather" -ForegroundColor White
Write-Host ""
Write-Host "[INFO] Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Inicia o servidor Flask
Set-Location "fase2\web_app"
& "$ProjectDir\.venv\Scripts\python.exe" app.py

# Se o servidor for interrompido
Write-Host ""
Write-Host "[INFO] Servidor encerrado." -ForegroundColor Yellow
pause
