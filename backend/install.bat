@echo off
echo ================================================
echo E-Commerce Recommendation System - Installation
echo ================================================
echo.

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies...
pip install fastapi uvicorn pydantic pydantic-settings email-validator python-jose passlib bcrypt python-dotenv httpx requests python-dateutil pytz joblib python-multipart Pillow aiocache

echo.
echo Installing optional ML libraries (may take time)...
pip install --only-binary :all: scikit-learn pandas numpy || echo Warning: ML libraries failed to install

echo.
echo ================================================
echo Installation complete!
echo ================================================
echo.
echo To run the application:
echo 1. call venv\Scripts\activate.bat
echo 2. python run.py
echo.
pause

