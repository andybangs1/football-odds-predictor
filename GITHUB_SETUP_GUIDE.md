# 🚀 GitHub Connection Setup Guide

## Step 1: Install Git

### Download Git for Windows
👉 **Visit:** https://git-scm.com/downloads

**For Windows (easiest option):**
1. Download Git for Windows
2. Run the installer (`.exe`)
3. Click "Next" through all steps
4. Select "Use Git from the Windows Command Prompt" (recommended)
5. Complete installation
6. **Restart your terminal**

### Verify Installation
```bash
git --version
```

—

## Step 2: Create a GitHub Repository

### Option A: Create on GitHub.com (Recommended)
1. Go to https://github.com
2. Sign in to your account (create one if needed)
3. Click **"+"** icon → **"New repository"**
4. **Repository name:** `football_odds_predictor`
5. **Description:** "Football match odds prediction system with AI analysis"
6. Choose **Public** or **Private**
7. **DO NOT** check "Initialize with README" (your project already has files)
8. Click **"Create repository"**

### Option B: Create from Command Line
If you have GitHub CLI installed:
```bash
gh repo create football_odds_predictor --public
```

—

## Step 3: Configure Git Locally

### Set Your Identity (ONE TIME ONLY)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Replace with your actual name and GitHub email address.

---

## Step 4: Initialize Local Repository

### Navigate to Project
```bash
cd "c:\Users\DELL\Desktop\Code with Ai\football_odds_predictor"
```

### Initialize Git
```bash
git init
```

### Create .gitignore File
Create a file named `.gitignore` in project root with this content:
```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# Flask
instance/
.webassets-cache

# Database
*.db
odds_history.db
football_odds.db

# Uploads
uploads/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local
```

### Add All Files
```bash
git add .
```

### Create Initial Commit
```bash
git commit -m "Initial commit: Football Odds Predictor with API endpoints"
```

---

## Step 5: Connect to GitHub

### Get Your GitHub Repo URL
1. Go to your GitHub.com repo
2. Click **"Code"** button (green, top right)
3. Copy the URL (either HTTPS or SSH):
   - **HTTPS:** `https://github.com/yourusername/football_odds_predictor.git`
   - **SSH:** `git@github.com:yourusername/football_odds_predictor.git`

### Add Remote Repository
Replace with your actual URL:
```bash
git remote add origin https://github.com/yourusername/football_odds_predictor.git
```

### First Push (Set Upstream)
```bash
git branch -M main
git push -u origin main
```

---

## Step 6: Verify Connection

### Check Remote is Set
```bash
git remote -v
```

Should output:
```
origin  https://github.com/yourusername/football_odds_predictor.git (fetch)
origin  https://github.com/yourusername/football_odds_predictor.git (push)
```

### Check on GitHub.com
Visit your repository URL - you should see all your files there!

---

## 🔐 Authentication

### For HTTPS (Recommended for Windows)
1. GitHub will ask for credentials first time
2. Use your GitHub username + **Personal Access Token** (not password)
3. Generate token at: https://github.com/settings/tokens
4. Windows will remember credentials (cached)

### For SSH (More Secure)
1. Generate SSH key:
```bash
ssh-keygen -t ed25519 -C "your.email@github.com"
```
2. Add public key to GitHub: https://github.com/settings/keys
3. Use SSH URL instead of HTTPS

---

## 📝 Future Commits

After the initial setup, you just need:

```bash
# Make changes to your files

# Stage changes
git add .

# Commit with message
git commit -m "Description of what changed"

# Push to GitHub
git push
```

---

## 📊 Quick Reference

```bash
# Initialize (ONE TIME)
git init
git remote add origin [YOUR_GITHUB_URL]

# Regular workflow
git add .
git commit -m "Your message"
git push

# Check status
git status

# View changes before committing
git diff

# See commit history
git log
```

---

## 🆘 Troubleshooting

### Error: "fatal: not a git repository"
**Solution:** Run `git init` first

### Error: "Permission denied (publickey)"
**Solution:** Use HTTPS instead of SSH, or add SSH key to GitHub

### Files not appearing on GitHub
**Solution:** Make sure you ran `git push` after commit

### .gitignore not working
**Solution:** Files may already be tracked. Remove and re-add:
```bash
git rm --cached [filename]
git add .
git commit -m "Remove [filename] from tracking"
```

---

## ✅ Complete Setup Checklist

- [ ] Installing Git from git-scm.com
- [ ] Restart terminal after Git installation
- [ ] Create GitHub account
- [ ] Create new repository on GitHub.com
- [ ] Configure Git username & email (`git config --global`)
- [ ] Navigate to project folder
- [ ] Run `git init`
- [ ] Create `.gitignore` file
- [ ] Run `git add .`
- [ ] Run `git commit -m "Initial commit..."`
- [ ] Copy GitHub repo URL
- [ ] Run `git remote add origin [URL]`
- [ ] Run `git branch -M main`
- [ ] Run `git push -u origin main`
- [ ] Verify files appear on GitHub.com

---

## 💡 Pro Tips

1. **Commit often** - Make small, meaningful commits
2. **Good messages** - Describe what and why, not just what
3. **Push regularly** - Don't wait until the end
4. **Use branches** - For features: `git checkout -b feature/new-feature`
5. **Pull before push** - Always get latest: `git pull`

---

## 📚 Need More Help?

- Git Basics: https://git-scm.com/book/en/v2/Getting-Started-Git-Basics
- GitHub Docs: https://docs.github.com/en
- GitHub Desktop: https://desktop.github.com/ (GUI alternative)

---

**Start with Step 1 and follow through. You'll be on GitHub in 10 minutes!**
