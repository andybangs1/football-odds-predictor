@echo off
echo ========================================
echo   Football Odds Predictor - Quick Deploy
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo After installing, run this script again.
    pause
    exit /b 1
)

echo [1/5] Checking Git configuration...
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    set /p username="Enter your name for Git: "
    git config --global user.name "%username%"
)

git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    set /p email="Enter your email for Git: "
    git config --global user.email "%email%"
)
echo    ✓ Git configured

echo.
echo [2/5] Initializing repository...
if not exist ".git" (
    git init
    echo    ✓ Repository initialized
) else (
    echo    ✓ Repository already exists
)

echo.
echo [3/5] Adding files to Git...
git add .
echo    ✓ Files staged

echo.
echo [4/5] Creating commit...
git commit -m "Ready for cloud deployment" >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✓ Commit created
) else (
    echo    ℹ No changes to commit (already up to date)
)

echo.
echo [5/5] Ready to push to GitHub!
echo.
echo ========================================
echo   NEXT STEPS:
echo ========================================
echo.
echo 1. Create GitHub repository:
echo    → Go to: https://github.com/new
echo    → Name: football-odds-predictor
echo    → Make it PUBLIC
echo    → Click "Create repository"
echo.
echo 2. Copy your repository URL
echo    Example: https://github.com/YOUR_USERNAME/football-odds-predictor.git
echo.
echo 3. Run these commands:
echo.
set /p repo_url="Paste your GitHub repository URL here (or press Enter to skip): "

if not "%repo_url%"=="" (
    echo.
    echo Adding remote repository...
    git remote remove origin >nul 2>&1
    git remote add origin %repo_url%
    git branch -M main
    
    echo Pushing to GitHub...
    git push -u origin main
    
    if %errorlevel% equ 0 (
        echo.
        echo ========================================
        echo   ✓ SUCCESS! Code pushed to GitHub
        echo ========================================
        echo.
        echo DEPLOY TO RENDER:
        echo 1. Go to: https://render.com
        echo 2. Sign up with GitHub
        echo 3. Click "New +" → "Web Service"
        echo 4. Select your repository
        echo 5. Click "Create Web Service"
        echo.
        echo Your app will be live in 5-7 minutes!
    ) else (
        echo.
        echo ERROR: Failed to push to GitHub
        echo.
        echo Try these steps manually:
        echo   git remote add origin %repo_url%
        echo   git branch -M main
        echo   git push -u origin main
    )
) else (
    echo.
    echo Manual push instructions:
    echo   git remote add origin YOUR_GITHUB_URL
    echo   git branch -M main
    echo   git push -u origin main
)

echo.
echo ========================================
echo Read DEPLOY_NOW.md for detailed guide!
echo ========================================
echo.
pause
