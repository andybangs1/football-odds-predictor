@echo off
color 0A
title Deploy to Cloud - Final Step!
cls

echo.
echo ========================================
echo   🎉 GITHUB UPLOAD COMPLETE!
echo ========================================
echo.
echo Your code is now on GitHub at:
echo https://github.com/andybangs1/football-odds-predictor
echo.
echo ========================================
echo   NEXT: DEPLOY TO THE INTERNET
echo ========================================
echo.
echo Let's make your app accessible to everyone!
echo.
echo Choose your hosting platform:
echo.
echo [1] Render.com ⭐ RECOMMENDED
echo     - Free forever for low traffic
echo     - Auto-deploys from GitHub
echo     - Professional URLs
echo     - Takes 5-7 minutes
echo.
echo [2] Replit 🚀 FASTEST
echo     - Live in 60 seconds
echo     - Free hosting
echo     - Instant URL
echo.
echo [3] Both (Render for main, Replit for testing)
echo.
set /p choice="Choose (1, 2, or 3): "

if "%choice%"=="1" goto render
if "%choice%"=="2" goto replit
if "%choice%"=="3" goto both
goto menu

:render
cls
echo.
echo ========================================
echo   DEPLOYING TO RENDER.COM
echo ========================================
echo.
echo Opening Render.com in your browser...
timeout /t 2 >nul
start https://render.com

cls
echo.
echo ========================================
echo   STEP-BY-STEP GUIDE
echo ========================================
echo.
echo On the Render.com website:
echo.
echo STEP 1: Sign Up
echo ---------------
echo 1. Click "Get Started" (top right)
echo 2. Choose "Sign up with GitHub"
echo 3. Use your andybangs1 account
echo 4. Click "Authorize Render"
echo.
echo STEP 2: Create Web Service
echo --------------------------
echo 1. Click the "New +" button (top right)
echo 2. Select "Web Service"
echo 3. Find "andybangs1/football-odds-predictor"
echo 4. Click "Connect"
echo.
echo STEP 3: Configure Settings
echo --------------------------
echo Fill in these fields:
echo.
echo   Name: football-odds-predictor
echo   Environment: Python 3
echo   Build Command: pip install -r requirements.txt
echo   Start Command: gunicorn app:app
echo   Instance Type: Free
echo.
echo STEP 4: Deploy
echo --------------
echo 1. Scroll down
echo 2. Click "Create Web Service"
echo 3. Wait 5-7 minutes (watch the logs)
echo.
echo STEP 5: Get Your URL
echo -------------------
echo Once deployed, your URL will be:
echo https://football-odds-predictor.onrender.com
echo.
echo (You'll see it at the top of your dashboard)
echo.
echo ========================================
echo.
echo Are you ready to check if it's live?
pause
echo.
echo Opening your app URL...
start https://football-odds-predictor.onrender.com
echo.
echo If you see your app, SUCCESS! 🎉
echo If not, wait a few more minutes and refresh.
echo.
goto success

:replit
cls
echo.
echo ========================================
echo   DEPLOYING TO REPLIT (FASTEST!)
echo ========================================
echo.
echo Opening Replit.com...
timeout /t 2 >nul
start https://replit.com

cls
echo.
echo ========================================
echo   SUPER SIMPLE STEPS
echo ========================================
echo.
echo On Replit.com:
echo.
echo 1. Sign in (or create account)
echo.
echo 2. Click "Create Repl" button
echo.
echo 3. Select "Import from GitHub"
echo.
echo 4. Paste this URL:
echo    https://github.com/andybangs1/football-odds-predictor
echo.
echo 5. Click "Import from GitHub"
echo.
echo 6. Wait for import (30 seconds)
echo.
echo 7. Click the big green "Run" button
echo.
echo 8. DONE! Your app is LIVE instantly!
echo.
echo 9. Replit gives you a URL like:
echo    https://football-odds-predictor.andybangs1.repl.co
echo.
echo Share that URL everywhere!
echo.
goto success

:both
cls
echo.
echo ========================================
echo   SMART STRATEGY: USE BOTH!
echo ========================================
echo.
echo Good choice! Here's why use both:
echo.
echo Render.com = Your main production app
echo   - More reliable
echo   - Better performance
echo   - Professional URL
echo.
echo Replit = Testing and development
echo   - Instant changes
echo   - Quick testing
echo   - Easy to experiment
echo.
echo Let's set up Render first (main app)...
pause
goto render

:success
cls
echo.
echo ========================================
echo   🎉🎉🎉 CONGRATULATIONS! 🎉🎉🎉
echo ========================================
echo.
echo YOUR APP IS NOW LIVE ON THE INTERNET!
echo.
echo ========================================
echo   WHAT YOU'VE ACCOMPLISHED:
echo ========================================
echo.
echo ✓ Built a Football Odds Predictor
echo ✓ Uploaded code to GitHub
echo ✓ Deployed to the cloud
echo ✓ Got a public URL
echo.
echo ========================================
echo   START MAKING MONEY 💰
echo ========================================
echo.
echo Step 1: Get Affiliate Links
echo ---------------------------
echo Sign up for betting affiliate programs:
echo - Betpawa Affiliates
echo - 1xbet Partners
echo - Bet365 Affiliates
echo.
echo Step 2: Share Your App
echo ----------------------
echo Post your URL on:
echo - Facebook groups
echo - WhatsApp status
echo - Twitter/X
echo - Instagram bio
echo.
echo Step 3: Add Predictions
echo -----------------------
echo 1. Open your app
echo 2. Upload betting screenshots
echo 3. Get AI predictions
echo 4. Share predictions with affiliate links
echo.
echo Step 4: Track Results
echo ---------------------
echo - Mark results as they come in
echo - System learns and improves
echo - Better predictions = more followers
echo - More followers = more affiliate earnings
echo.
echo ========================================
echo   YOUR LINKS:
echo ========================================
echo.
echo GitHub: https://github.com/andybangs1/football-odds-predictor
echo.
echo Render: https://football-odds-predictor.onrender.com
echo (or your custom URL)
echo.
echo ========================================
echo   NEED HELP?
echo ========================================
echo.
echo Check these files in your project:
echo - MONETIZATION.md (how to make money)
echo - HOW_TO_USE_PREDICTIONS.md (usage guide)
echo - VALUE_BETTING_GUIDE.md (betting strategy)
echo.
echo ========================================
echo   UPDATES ^& MAINTENANCE
echo ========================================
echo.
echo To update your app:
echo 1. Make changes to code
echo 2. Run: git add .
echo 3. Run: git commit -m "Updated feature"
echo 4. Run: git push
echo 5. Render auto-deploys in 2-3 minutes!
echo.
echo ========================================
echo.
echo Ready to make your first prediction?
set /p open="Open your live app now? (y/n): "
if /i "%open%"=="y" start https://football-odds-predictor.onrender.com
echo.
echo Good luck and happy earning! 💰🎉🚀
echo.
pause
exit
