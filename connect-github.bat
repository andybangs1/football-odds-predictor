@echo off
color 0A
title GitHub Connection Helper - andybangs1
cls

echo.
echo ========================================
echo   GITHUB CONNECTION HELPER
echo ========================================
echo   Account: andybangs1
echo   Repository: football-odds-predictor
echo ========================================
echo.
echo Having trouble connecting? Let's fix it!
echo.
echo Choose the EASIEST method for you:
echo.
echo [1] GitHub Desktop (EASIEST - Recommended!)
echo     - No commands needed
echo     - Automatic authentication
echo     - Visual interface
echo.
echo [2] Personal Access Token (Manual)
echo     - Generate a token on GitHub
echo     - Use as password when pushing
echo.
echo [3] Check what's wrong
echo     - Diagnose connection issues
echo.
echo [0] Exit
echo.
set /p choice="Enter your choice (1, 2, 3, or 0): "

if "%choice%"=="1" goto github_desktop
if "%choice%"=="2" goto token_method
if "%choice%"=="3" goto diagnose
if "%choice%"=="0" exit
goto menu

:github_desktop
cls
echo.
echo ========================================
echo   METHOD 1: GitHub Desktop (EASIEST!)
echo ========================================
echo.
echo This is the easiest way - no commands needed!
echo.
echo Step 1: Download GitHub Desktop
echo ---------------------------------
echo Opening download page...
timeout /t 2 >nul
start https://desktop.github.com
echo.
echo Step 2: Install and Sign In
echo ---------------------------
echo 1. Install GitHub Desktop
echo 2. Open it and click "Sign in to GitHub.com"
echo 3. Enter username: andybangs1
echo 4. Enter your GitHub password
echo 5. Click "Authorize desktop"
echo.
echo Step 3: Add This Repository
echo ---------------------------
echo 1. In GitHub Desktop, click "Add" dropdown
echo 2. Choose "Add existing repository"
echo 3. Browse to: C:\Users\DELL\Desktop\Code with Ai\football_odds_predictor
echo 4. Click "Add repository"
echo.
echo Step 4: Create Repository on GitHub
echo -----------------------------------
echo 1. In GitHub Desktop, click "Publish repository"
echo 2. Name: football-odds-predictor
echo 3. UNCHECK "Keep this code private" (must be Public for free hosting)
echo 4. Click "Publish repository"
echo.
echo ✓ DONE! Your code is now on GitHub!
echo.
echo Your repository will be at:
echo https://github.com/andybangs1/football-odds-predictor
echo.
pause
goto deploy_next

:token_method
cls
echo.
echo ========================================
echo   METHOD 2: Personal Access Token
echo ========================================
echo.
echo Step 1: First, create repository on GitHub
echo ------------------------------------------
echo 1. Opening GitHub new repository page...
timeout /t 2 >nul
start https://github.com/new
echo.
echo 2. On the page that opens:
echo    - Repository name: football-odds-predictor
echo    - Description: AI-powered football odds predictor
echo    - Choose: PUBLIC (required for free hosting)
echo    - DON'T check "Add a README file"
echo    - Click "Create repository"
echo.
pause
echo.
echo Step 2: Generate Personal Access Token
echo --------------------------------------
echo Opening token generation page...
timeout /t 2 >nul
start https://github.com/settings/tokens/new
echo.
echo On the page that opens:
echo 1. Note: "Football Odds Predictor"
echo 2. Expiration: 90 days (or No expiration)
echo 3. Check the box: [x] repo (all checkboxes under it)
echo 4. Scroll down and click "Generate token"
echo 5. COPY THE TOKEN (you'll only see it once!)
echo.
pause
echo.
echo Step 3: Push to GitHub
echo ---------------------
echo Now we'll push your code...
echo When it asks for:
echo   Username: andybangs1
echo   Password: PASTE YOUR TOKEN (right-click to paste)
echo.
pause
echo.
echo Pushing to GitHub...
git push -u origin main
echo.
if %errorlevel% equ 0 (
    echo ✓ SUCCESS! Code pushed to GitHub
    echo.
    echo View your repository:
    start https://github.com/andybangs1/football-odds-predictor
    pause
    goto deploy_next
) else (
    echo ❌ Push failed. Let's try to diagnose...
    pause
    goto diagnose
)

:diagnose
cls
echo.
echo ========================================
echo   DIAGNOSING CONNECTION...
echo ========================================
echo.
echo Checking your Git configuration...
echo.
git config --list | findstr "user"
echo.
echo Checking remote repository...
echo.
git remote -v
echo.
echo Checking repository status...
echo.
git status
echo.
echo ========================================
echo   COMMON ISSUES & SOLUTIONS
echo ========================================
echo.
echo Issue 1: "Repository not found"
echo --------------------------------
echo Solution: You need to create the repository on GitHub first!
echo Go to: https://github.com/new
echo Name it: football-odds-predictor
echo Make it PUBLIC
echo.
echo Issue 2: "Authentication failed"
echo ---------------------------------
echo Solution: Don't use your GitHub password!
echo You MUST use a Personal Access Token
echo Generate one at: https://github.com/settings/tokens/new
echo.
echo Issue 3: "Permission denied"
echo ----------------------------
echo Solution: Make sure you're logged in as andybangs1
echo Or use GitHub Desktop (handles auth automatically)
echo.
echo Issue 4: "Could not read from remote"
echo -------------------------------------
echo Solution: Check your internet connection
echo Or try using GitHub Desktop
echo.
echo ========================================
echo.
set /p retry="Would you like to try again? (y/n): "
if /i "%retry%"=="y" goto menu
exit

:deploy_next
cls
echo.
echo ========================================
echo   ✓ CONNECTED TO GITHUB!
echo ========================================
echo.
echo Your repository: https://github.com/andybangs1/football-odds-predictor
echo.
echo ========================================
echo   NEXT: Deploy to Cloud
echo ========================================
echo.
echo Now let's make your app available on the internet!
echo.
echo Choose a hosting platform:
echo.
echo [1] Render.com (Recommended)
echo     - Free forever for low traffic
echo     - Auto-deploys from GitHub
echo     - Professional URLs
echo     - URL: football-odds-predictor.onrender.com
echo.
echo [2] Replit (Fastest)
echo     - Instant deployment
echo     - Free
echo     - URL: auto-generated
echo.
set /p deploy_choice="Which platform? (1 or 2): "

if "%deploy_choice%"=="1" goto render
if "%deploy_choice%"=="2" goto replit
exit

:render
cls
echo.
echo ========================================
echo   DEPLOYING TO RENDER.COM
echo ========================================
echo.
echo Opening Render.com...
start https://render.com
echo.
echo Follow these steps:
echo.
echo 1. Click "Get Started" and sign up with GitHub
echo 2. Authorize Render to access your repositories
echo 3. Click "New +" then "Web Service"
echo 4. Find and select: andybangs1/football-odds-predictor
echo 5. Configure:
echo    - Name: football-odds-predictor
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn app:app
echo    - Instance Type: Free
echo 6. Click "Create Web Service"
echo 7. Wait 5-7 minutes for deployment
echo.
echo Your app will be live at:
echo https://football-odds-predictor.onrender.com
echo.
echo (The exact URL will be shown in Render dashboard)
echo.
pause
exit

:replit
cls
echo.
echo ========================================
echo   DEPLOYING TO REPLIT
echo ========================================
echo.
echo Opening Replit...
start https://replit.com
echo.
echo Follow these steps:
echo.
echo 1. Sign in to Replit
echo 2. Click "Create Repl"
echo 3. Select "Import from GitHub"
echo 4. Paste: https://github.com/andybangs1/football-odds-predictor
echo 5. Click "Import from GitHub"
echo 6. Wait for import to complete
echo 7. Click the big "Run" button
echo 8. Your app is LIVE! (instant URL provided)
echo.
echo Share the URL and start making money! 💰
echo.
pause
exit
