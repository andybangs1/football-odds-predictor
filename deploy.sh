#!/bin/bash

echo "========================================"
echo "  Football Odds Predictor - Quick Deploy"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed!"
    echo ""
    echo "Install Git:"
    echo "  Mac: brew install git"
    echo "  Linux: sudo apt-get install git"
    exit 1
fi

echo "[1/5] Checking Git configuration..."
if ! git config user.name &> /dev/null; then
    read -p "Enter your name for Git: " username
    git config --global user.name "$username"
fi

if ! git config user.email &> /dev/null; then
    read -p "Enter your email for Git: " email
    git config --global user.email "$email"
fi
echo "   ✓ Git configured"

echo ""
echo "[2/5] Initializing repository..."
if [ ! -d ".git" ]; then
    git init
    echo "   ✓ Repository initialized"
else
    echo "   ✓ Repository already exists"
fi

echo ""
echo "[3/5] Adding files to Git..."
git add .
echo "   ✓ Files staged"

echo ""
echo "[4/5] Creating commit..."
git commit -m "Ready for cloud deployment" &> /dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ Commit created"
else
    echo "   ℹ No changes to commit (already up to date)"
fi

echo ""
echo "[5/5] Ready to push to GitHub!"
echo ""
echo "========================================"
echo "  NEXT STEPS:"
echo "========================================"
echo ""
echo "1. Create GitHub repository:"
echo "   → Go to: https://github.com/new"
echo "   → Name: football-odds-predictor"
echo "   → Make it PUBLIC"
echo "   → Click 'Create repository'"
echo ""
read -p "Enter your GitHub repository URL (or press Enter to skip): " repo_url

if [ -n "$repo_url" ]; then
    echo ""
    echo "Adding remote repository..."
    git remote remove origin 2>/dev/null
    git remote add origin "$repo_url"
    git branch -M main
    
    echo "Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "========================================"
        echo "  ✓ SUCCESS! Code pushed to GitHub"
        echo "========================================"
        echo ""
        echo "DEPLOY TO RENDER:"
        echo "1. Go to: https://render.com"
        echo "2. Sign up with GitHub"
        echo "3. Click 'New +' → 'Web Service'"
        echo "4. Select your repository"
        echo "5. Click 'Create Web Service'"
        echo ""
        echo "Your app will be live in 5-7 minutes!"
    else
        echo ""
        echo "ERROR: Failed to push to GitHub"
        echo ""
        echo "Try these steps manually:"
        echo "  git remote add origin $repo_url"
        echo "  git branch -M main"
        echo "  git push -u origin main"
    fi
else
    echo ""
    echo "Manual push instructions:"
    echo "  git remote add origin YOUR_GITHUB_URL"
    echo "  git branch -M main"
    echo "  git push -u origin main"
fi

echo ""
echo "========================================"
echo "Read DEPLOY_NOW.md for detailed guide!"
echo "========================================"
echo ""
