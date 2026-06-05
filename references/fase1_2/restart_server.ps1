# ============================================
# Script PowerShell - Restart Servidor Flask
# FarmTech Solutions - Sistema de Irrigação
# ============================================

Write-Host ""
Write-Host "========================================"
Write-Host "  FarmTech Solutions - Restart Servidor"
Write-Host "========================================"
Write-Host ""

Write-Host "[INFO] Procurando processos Python do Flask..." -ForegroundColor Cyan

# Mata todos os processos python.exe relacionados ao Flask
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue

if ($pythonProcesses) {
    Write-Host "[INFO] Encerrando $($pythonProcesses.Count) processo(s) Python..." -ForegroundColor Yellow
    $pythonProcesses | Stop-Process -Force
    Write-Host "[INFO] Servidor Flask encerrado" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "[INFO] Nenhum servidor Flask em execução" -ForegroundColor Yellow
}

Write-Host "[INFO] Iniciando novo servidor..." -ForegroundColor Green
Write-Host ""

# Chama o script de start
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$scriptDir\start_server.ps1"
