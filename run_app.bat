@echo off
echo ========================================================
echo   Launching AddictionSense Full-Stack Web Application
echo ========================================================
echo.
echo 1. Starting Flask Backend Server (http://127.0.0.1:5000)...
start "AddictionSense Flask Backend" cmd /k "python backend/app.py"

echo 2. Waiting 3 seconds for server initialization...
timeout /t 3 /nobreak >nul

echo 3. Opening Frontend UI Portal in Web Browser...
start "" "%~dp0frontend\dashboard.html"

echo.
echo Setup Complete! The application is live.
pause
