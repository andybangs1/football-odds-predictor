@echo off
color 0C
cls
echo.
echo ========================================
echo   ERROR 500 - REPOSITORY DOESN'T EXIST
echo ========================================
echo.
echo The problem: You're trying to push to a GitHub
echo repository that doesn't exist yet!
echo.
echo ========================================
echo   SOLUTION: Create Repository First
echo ========================================
echo.
echo I'll open GitHub for you in 3 seconds...
echo.
timeout /t 3 >nul

start https://github.com/new

cls
echo.
echo ========================================
echo   CREATE YOUR REPOSITORY ON GITHUB
echo ========================================
echo.
echo On the page that just opened, do this:
echo.
echo 1. Repository name: football-odds-predictor
echo    (type exactly this, no spaces)
echo.
echo 2. Description: AI Football Odds Predictor
echo    (optional)
echo.
echo 3. Choose: PUBLIC (must be public for free hosting)
echo    ● Public  ○ Private  ^<--- Choose Public
echo.
echo 4. IMPORTANT: Do NOT check any boxes!
echo    Don't add README, .gitignore, or license
echo    Leave everything UNCHECKED
echo.
echo 5. Click "Create repository" button
echo.
echo ========================================
echo.
set /p created="Did you create the repository? (y/n): "

if /i "%created%"=="y" goto push_now
if /i "%created%"=="n" goto alternative
goto end

:push_now
cls
echo.
echo ========================================
echo   PUSHING TO GITHUB
echo ========================================
echo.
echo Great! Now we'll push your code...
echo.
echo When it asks for credentials:
echo   Username: andybangs1
echo   Password: Use Personal Access Token (NOT your password)
echo.
echo Don't have a token? I'll help you create one.
set /p has_token="Do you have a Personal Access Token? (y/n): "

if /i "%has_token%"=="n" goto create_token

echo.
echo Pushing to GitHub...
echo.
git push -u origin main

if %errorlevel% equ 0 (
    cls
    echo.
    echo ========================================
    echo   ✓✓✓ SUCCESS! ✓✓✓
    echo ========================================
    echo.
    echo Your code is now on GitHub!
    echo.
    start https://github.com/andybangs1/football-odds-predictor
    echo.
    echo Opening your repository...
    echo.
    echo ========================================
    echo   NEXT: DEPLOY TO INTERNET
    echo ========================================
    echo.
    set /p deploy="Ready to deploy to Render.com? (y/n): "
    if /i "%deploy%"=="y" goto deploy_render
    exit
) else (
    echo.
    echo ❌ Push failed. This is usually an authentication issue.
    echo.
    set /p retry="Try creating a token? (y/n): "
    if /i "%retry%"=="y" goto create_token
    goto alternative
)

:create_token
cls
echo.
echo ========================================
echo   CREATE PERSONAL ACCESS TOKEN
echo ========================================
echo.
echo Opening token creation page...
timeout /t 2 >nul
start https://github.com/settings/tokens/new

cls
echo.
echo On the page that opened:
echo.
echo 1. Token name: Football Odds Predictor
echo 2. Expiration: 90 days (or No expiration)
echo 3. Select scopes: Check [x] repo (check the main box)
echo 4. Scroll down and click "Generate token"
echo 5. COPY THE TOKEN (you'll only see it once!)
echo.
echo ========================================
echo.
pause
echo.
echo Now let's push with your token...
echo.
echo When prompted:
echo   Username: andybangs1
echo   Password: PASTE YOUR TOKEN (right-click to paste)
echo.
pause
echo.

git push -u origin main

if %errorlevel% equ 0 (
    cls
    echo.
    echo ========================================
    echo   ✓✓✓ SUCCESS! ✓✓✓
    echo ========================================
    echo.
    echo Your code is now on GitHub!
    start https://github.com/andybangs1/football-odds-predictor
    echo.
    set /p deploy="Ready to deploy to Render.com? (y/n): "
    if /i "%deploy%"=="y" goto deploy_render
) else (
    echo ❌ Still having issues? Try the easier method...
    pause
    goto alternative
)
exit

:alternative
cls
echo.
echo ========================================
echo   EASIER METHOD: GITHUB DESKTOP
echo ========================================
echo.
echo Forget about tokens and commands!
echo Use GitHub Desktop instead (much easier).
echo.
echo Opening download page...
timeout /t 2 >nul
start https://desktop.github.com

cls
echo.
echo After installing GitHub Desktop:
echo.
echo 1. Sign in with your GitHub account (andybangs1)
echo 2. File → Add local repository
echo 3. Choose this folder:
echo    C:\Users\DELL\Desktop\Code with Ai\football_odds_predictor
echo 4. Click "Publish repository"
echo 5. Make sure it's PUBLIC
echo 6. Done!
echo.
echo GitHub Desktop handles all authentication automatically.
echo No tokens, no errors, no hassle!
echo.
pause
exit

:deploy_render
cls
echo.
echo ========================================
echo   DEPLOY TO RENDER.COM
echo ========================================
echo.
echo Opening Render...
timeout /t 2 >nul
start https://render.com

cls
echo.
echo On Render.com:
echo.
echo 1. Click "Get Started"
echo 2. Sign up with GitHub (as andybangs1)
echo 3. Click "New +" → "Web Service"
echo 4. Select: andybangs1/football-odds-predictor
echo 5. Click "Connect"
echo 6. Settings:
echo    - Name: football-odds-predictor
echo    - Build: pip install -r requirements.txt
echo    - Start: gunicorn app:app
echo    - Type: Free
echo 7. Click "Create Web Service"
echo.
echo Wait 5-7 minutes for deployment...
echo.
echo Your app will be live at:
echo https://football-odds-predictor.onrender.com
echo.
echo ========================================
echo   🎉 ALL DONE!
echo ========================================
echo.
pause
exit

:end
exit
