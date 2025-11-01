@echo off
echo ============================================================
echo Starting E-Commerce Backend Server
echo ============================================================
echo.

cd /d "%~dp0"

echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

echo [INFO] Starting uvicorn server...
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
