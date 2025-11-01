# PowerShell script to start backend
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting E-Commerce Backend Server" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "[INFO] Starting uvicorn server..." -ForegroundColor Green
Write-Host ""

# Start backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
