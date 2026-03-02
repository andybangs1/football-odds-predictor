@echo off
color 0B
cls
echo.
echo ========================================
echo   SIMPLE FIX - No Technical Skills Needed
echo ========================================
echo.
echo I'll open everything you need - just follow along!
echo.
pause

REM Step 1: Open GitHub Desktop download
echo.
echo ========================================
echo   Step 1: Download GitHub Desktop
echo ========================================
echo.
echo Opening download page...
echo This is the EASIEST way - no commands needed!
echo.
timeout /t 2 >nul
start https://desktop.github.com/
echo.
echo ACTION REQUIRED:
echo 1. Download GitHub Desktop
echo 2. Install it (just click Next, Next, Finish)
echo 3. Come back here when done
echo.
pause

REM Step 2: Instructions for GitHub Desktop
cls
echo.
echo ========================================
echo   Step 2: Sign In to GitHub Desktop
echo ========================================
echo.
echo Now open GitHub Desktop and:
echo.
echo 1. Click "Sign in to GitHub.com"
echo 2. Your browser will open
echo 3. Enter username: andybangs1
echo 4. Enter your GitHub password
echo 5. Click "Authorize desktop"
echo.
echo Done? Press any key...
pause >nul

cls
echo.
echo ========================================
echo   Step 3: Add Your Project
echo ========================================
echo.
echo In GitHub Desktop:
echo.
echo 1. Click "File" menu (top left)
echo 2. Choose "Add local repository"
echo 3. Click "Choose..." button
echo 4. Browse to this folder:
echo    C:\Users\DELL\Desktop\Code with Ai\football_odds_predictor
echo 5. Click "Add repository"
echo.
echo Done? Press any key...
pause >nul

cls
echo.
echo ========================================
echo   Step 4: Publish to GitHub
echo ========================================
echo.
echo In GitHub Desktop:
echo.
echo 1. You'll see a "Publish repository" button
echo 2. Click it
echo 3. Repository name should be: football-odds-predictor
echo 4. IMPORTANT: UNCHECK "Keep this code private"
echo    (It must be PUBLIC for free hosting)
echo 5. Click "Publish repository"
echo.
echo Done? Press any key...
pause >nul

cls
echo.
echo ========================================
echo   ✓ SUCCESS!
echo ========================================
echo.
echo Your code is now on GitHub!
echo.
echo Opening your repository...
timeout /t 2 >nul
start https://github.com/andybangs1/football-odds-predictor
echo.
echo You should see all your files!
echo.
echo ========================================
echo   NEXT: Deploy to Internet
echo ========================================
echo.
echo Your app is on GitHub, now let's make it live!
echo.
set /p deploy="Ready to deploy? (y/n): "
if /i "%deploy%"=="y" goto deploy
exit

:deploy
cls
echo.
echo ========================================
echo   Deploy to Render.com (FREE)
echo ========================================
echo.
echo Opening Render.com...
timeout /t 2 >nul
start https://render.com/
echo.
echo On the Render website:
echo.
echo 1. Click "Get Started" (top right)
echo 2. Choose "Sign up with GitHub"
echo 3. Authorize Render
echo 4. Click "New +" (top right)
echo 5. Choose "Web Service"
echo 6. Find: andybangs1/football-odds-predictor
echo 7. Click "Connect"
echo 8. Settings:
echo    - Name: football-odds-predictor
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn app:app
echo    - Instance Type: Free
echo 9. Click "Create Web Service"
echo.
echo Wait 5-7 minutes...
echo.
echo Your app will be live at:
echo https://football-odds-predictor.onrender.com
echo.
echo ========================================
echo   🎉 ALL DONE!
echo ========================================
echo.
echo Your app is now:
echo ✓ On GitHub: https://github.com/andybangs1/football-odds-predictor
echo ✓ Living on the internet
echo ✓ Ready to share and make money!
echo.
pause
exit
