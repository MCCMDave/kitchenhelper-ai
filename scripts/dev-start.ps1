# ============================================
# KitchenHelper-AI Development Start Script
# For Windows PowerShell
# ============================================

param(
    [switch]$Docker,
    [switch]$Build,
    [switch]$Stop,
    [switch]$Logs,
    [switch]$Help
)

# Colors
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Cyan = "Cyan"

function Show-Help {
    Write-Host "`n========================================" -ForegroundColor $Cyan
    Write-Host "  KitchenHelper-AI Dev Script" -ForegroundColor $Cyan
    Write-Host "========================================" -ForegroundColor $Cyan
    Write-Host "`nUsage:" -ForegroundColor $Yellow
    Write-Host "  .\dev-start.ps1           Start local dev server (uvicorn)"
    Write-Host "  .\dev-start.ps1 -Docker   Start in Docker container"
    Write-Host "  .\dev-start.ps1 -Build    Rebuild Docker image"
    Write-Host "  .\dev-start.ps1 -Stop     Stop Docker containers"
    Write-Host "  .\dev-start.ps1 -Logs     View Docker logs"
    Write-Host "  .\dev-start.ps1 -Help     Show this help"
    Write-Host ""
}

function Start-LocalDev {
    Write-Host "`n[*] Starting local development server..." -ForegroundColor $Green

    # Navigate to backend (go up one level from scripts/)
    $projectRoot = Split-Path -Parent $PSScriptRoot
    $backendPath = Join-Path $projectRoot "backend"
    Set-Location $backendPath

    # Check if venv exists
    $venvPath = Join-Path $backendPath "venv\Scripts\Activate.ps1"
    if (-not (Test-Path $venvPath)) {
        Write-Host "[!] Virtual environment not found!" -ForegroundColor $Red
        Write-Host "    Run: python -m venv venv" -ForegroundColor $Yellow
        Write-Host "    Then: .\venv\Scripts\Activate.ps1" -ForegroundColor $Yellow
        Write-Host "    Then: pip install -r requirements.txt" -ForegroundColor $Yellow
        exit 1
    }

    # Activate venv and start uvicorn
    Write-Host "[*] Activating virtual environment..." -ForegroundColor $Yellow
    & $venvPath

    Write-Host "[*] Starting uvicorn..." -ForegroundColor $Yellow
    Write-Host ""
    Write-Host "========================================" -ForegroundColor $Green
    Write-Host "  API:  http://127.0.0.1:8000" -ForegroundColor $Cyan
    Write-Host "  Docs: http://127.0.0.1:8000/docs" -ForegroundColor $Cyan
    Write-Host "  Press Ctrl+C to stop" -ForegroundColor $Yellow
    Write-Host "========================================" -ForegroundColor $Green
    Write-Host ""

    uvicorn app.main:app --reload
}

function Start-Docker {
    Write-Host "`n[*] Starting Docker container..." -ForegroundColor $Green
    $projectRoot = Split-Path -Parent $PSScriptRoot
    Set-Location $projectRoot

    # Check for .env file
    if (-not (Test-Path ".env")) {
        Write-Host "[!] .env file not found!" -ForegroundColor $Yellow
        Write-Host "    Copying from .env.example..." -ForegroundColor $Yellow
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" ".env"
            Write-Host "[OK] .env created. Please edit it with your settings." -ForegroundColor $Green
        } else {
            Write-Host "[!] .env.example not found either!" -ForegroundColor $Red
            exit 1
        }
    }

    docker compose up -d

    Write-Host "`n========================================" -ForegroundColor $Green
    Write-Host "  Container started!" -ForegroundColor $Cyan
    Write-Host "  API:  http://localhost:8000" -ForegroundColor $Cyan
    Write-Host "  Docs: http://localhost:8000/docs" -ForegroundColor $Cyan
    Write-Host "========================================" -ForegroundColor $Green
    Write-Host "`n[*] View logs with: .\dev-start.ps1 -Logs" -ForegroundColor $Yellow
}

function Build-Docker {
    Write-Host "`n[*] Building Docker image..." -ForegroundColor $Green
    $projectRoot = Split-Path -Parent $PSScriptRoot
    Set-Location $projectRoot
    docker compose build --no-cache
    Write-Host "[OK] Build complete!" -ForegroundColor $Green
}

function Stop-Docker {
    Write-Host "`n[*] Stopping Docker containers..." -ForegroundColor $Yellow
    $projectRoot = Split-Path -Parent $PSScriptRoot
    Set-Location $projectRoot
    docker compose down
    Write-Host "[OK] Containers stopped!" -ForegroundColor $Green
}

function Show-Logs {
    Write-Host "`n[*] Showing Docker logs (Ctrl+C to exit)..." -ForegroundColor $Yellow
    $projectRoot = Split-Path -Parent $PSScriptRoot
    Set-Location $projectRoot
    docker compose logs -f
}

# Main
if ($Help) {
    Show-Help
} elseif ($Docker) {
    Start-Docker
} elseif ($Build) {
    Build-Docker
} elseif ($Stop) {
    Stop-Docker
} elseif ($Logs) {
    Show-Logs
} else {
    Start-LocalDev
}
