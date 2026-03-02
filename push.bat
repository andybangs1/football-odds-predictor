@echo off
echo ========================================
echo   Push to GitHub - andybangs1
echo ========================================
echo.
echo Your repository: https://github.com/andybangs1/football-odds-predictor
echo.
echo Before running this script, make sure you:
echo 1. Created the repository on GitHub
echo 2. Visit: https://github.com/new
echo 3. Name it: football-odds-predictor
echo 4. Make it PUBLIC
echo 5. Click "Create repository"
echo.
pause
echo.
echo ========================================
echo   Pushing to GitHub...
echo ========================================
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   ✓ SUCCESS! Code pushed to GitHub
    echo ========================================
    echo.
    echo View your repository:
    echo https://github.com/andybangs1/football-odds-predictor
    echo.
    echo ========================================
    echo   NEXT: Deploy to Cloud
    echo ========================================
    echo.
    echo Option 1 - Render.com (Recommended):
    echo   1. Go to: https://render.com
    echo   2. Sign up with GitHub
    echo   3. Click "New +" then "Web Service"
    echo   4. Select your repository
    echo   5. Click "Create Web Service"
    echo   6. Wait 5-7 minutes
    echo   7. Your app will be live!
    echo.
    echo Option 2 - Replit (Fastest):
    echo   1. Go to: https://replit.com
    echo   2. Click "Import from GitHub"
    echo   3. Paste: https://github.com/andybangs1/football-odds-predictor
    echo   4. Click "Run"
    echo   5. Done! Instant URL!
    echo.
    start https://github.com/andybangs1/football-odds-predictor
) else (
    echo.
    echo ========================================
    echo   ❌ Push Failed
    echo ========================================
    echo.
    echo Common solutions:
    echo.
    echo 1. Authentication Error:
    echo    - Don't use your GitHub password
    echo    - Generate Personal Access Token:
    echo      https://github.com/settings/tokens/new
    echo    - Use token as password
    echo.
    echo 2. Repository Not Found:
    echo    - Create repo first: https://github.com/new
    echo    - Name: football-odds-predictor
    echo    - Make it PUBLIC
    echo.
    echo 3. Use GitHub Desktop (Easier):
    echo    - Download: https://desktop.github.com
    echo    - Sign in as andybangs1
    echo    - Handles auth automatically
    echo.
    echo Read PUSH_TO_GITHUB.md for detailed help
)

echo.
pause
