@echo off
REM KitchenHelper Backend Stop Script
REM Stops all Python processes using port 8000

echo.
echo ======================================
echo KitchenHelper Backend - Stop Script
echo ======================================
echo.

echo Checking for processes on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do (
    echo Found process: %%a
    echo Terminating process %%a...
    taskkill /F /PID %%a
    if errorlevel 1 (
        echo ERROR: Could not terminate process %%a
    ) else (
        echo Process %%a terminated successfully
    )
)

echo.
echo Verifying port 8000 is free...
netstat -ano | findstr ":8000.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo Port 8000 is now free!
    echo.
    echo Backend stopped successfully.
) else (
    echo WARNING: Port 8000 is still in use!
    echo Please close Python/Uvicorn manually.
)

echo.
pause
