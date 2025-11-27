# ============================================
# KitchenHelper-AI Log Viewer Script
# For Windows PowerShell
# ============================================

param(
    [int]$Lines = 100,
    [switch]$Follow,
    [switch]$All,
    [switch]$Help
)

$Cyan = "Cyan"
$Yellow = "Yellow"
$Green = "Green"

function Show-Help {
    Write-Host "`n========================================" -ForegroundColor $Cyan
    Write-Host "  KitchenHelper-AI Log Viewer" -ForegroundColor $Cyan
    Write-Host "========================================" -ForegroundColor $Cyan
    Write-Host "`nUsage:" -ForegroundColor $Yellow
    Write-Host "  .\logs-view.ps1             Show last 100 lines"
    Write-Host "  .\logs-view.ps1 -Lines 50   Show last 50 lines"
    Write-Host "  .\logs-view.ps1 -Follow     Follow logs in real-time"
    Write-Host "  .\logs-view.ps1 -All        Show all logs"
    Write-Host "  .\logs-view.ps1 -Help       Show this help"
    Write-Host ""
}

function Show-DockerLogs {
    $projectRoot = Split-Path -Parent $PSScriptRoot
    Set-Location $projectRoot

    # Check if container is running
    $running = docker compose ps --services --filter "status=running" 2>$null
    if (-not $running) {
        Write-Host "[!] No containers running!" -ForegroundColor $Yellow
        Write-Host "    Start with: .\scripts\dev-start.ps1 -Docker" -ForegroundColor $Yellow
        exit 1
    }

    Write-Host "`n[*] KitchenHelper-AI Logs" -ForegroundColor $Green
    Write-Host "    Press Ctrl+C to exit`n" -ForegroundColor $Yellow

    if ($Follow) {
        docker compose logs -f
    } elseif ($All) {
        docker compose logs
    } else {
        docker compose logs --tail=$Lines
    }
}

# Main
if ($Help) {
    Show-Help
} else {
    Show-DockerLogs
}
