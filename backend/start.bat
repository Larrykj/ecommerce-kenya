@echo off
echo ================================================
echo Starting E-Commerce Recommendation System
echo ================================================
echo.

if not exist "venv\" (
    echo Error: Virtual environment not found!
    echo Please run install.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python run.py

