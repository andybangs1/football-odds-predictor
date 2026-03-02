@echo off
REM Football Odds Predictor - Easy Start Script
REM This script installs dependencies and starts the app

echo.
echo ============================================
echo  Football Odds Predictor Launcher
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from: https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [✓] Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [!] Creating virtual environment...
    python -m venv venv
    echo [✓] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [!] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [!] Checking dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo [✓] Dependencies installed
echo.

REM Check for Tesseract
echo [!] Checking for Tesseract OCR...
python -c "import pytesseract; pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'; pytesseract.image_to_string" >nul 2>&1
if errorlevel 1 (
    echo [⚠] WARNING: Tesseract OCR not found
    echo You can still use the app, but OCR features will be limited
    echo Install from: https://github.com/UB-Mannheim/tesseract/wiki
    echo.
) else (
    echo [✓] Tesseract OCR found
    echo.
)

REM Start the app
echo [!] Starting Football Odds Predictor...
echo.
echo ============================================
echo  Opening http://localhost:5000
echo  Press Ctrl+C to stop the server
echo ============================================
echo.

python app.py
pause
