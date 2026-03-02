#!/bin/bash

# Football Odds Predictor - Easy Start Script for Linux/Mac
# This script installs dependencies and starts the app

echo ""
echo "============================================"
echo " Football Odds Predictor Launcher"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ using:"
    echo "  Mac: brew install python3"
    echo "  Linux: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo "[✓] Python found"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[!] Creating virtual environment..."
    python3 -m venv venv
    echo "[✓] Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "[!] Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "[!] Installing dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "[✓] Dependencies installed"
echo ""

# Check for Tesseract
echo "[!] Checking for Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    echo "[✓] Tesseract OCR found"
    echo ""
else
    echo "[⚠] WARNING: Tesseract OCR not found"
    echo "You can still use the app, but OCR features will be limited"
    echo "Install using:"
    echo "  Mac: brew install tesseract"
    echo "  Linux: sudo apt-get install tesseract-ocr"
    echo ""
fi

# Start the app
echo "[!] Starting Football Odds Predictor..."
echo ""
echo "============================================"
echo " Opening http://localhost:5000"
echo " Press Ctrl+C to stop the server"
echo "============================================"
echo ""

python app.py
