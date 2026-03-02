# 🚀 Quick Start - Connect to GitHub in 5 Minutes

## Prerequisites: Install Git First!

### Step 1: Download & Install Git (3 minutes)
👉 **Visit:** https://git-scm.com/download/win

1. Download Git for Windows
2. Run installer
3. Click "Next" through all screens
4. Default options are fine
5. **Restart your terminal after installation**

---

## After Git is Installed:

### Step 2: Create GitHub Repository (2 minutes)

1. Go to https://github.com
2. Sign in (create account if needed)
3. Click **"+"** → **"New repository"**
4. Name: `football_odds_predictor`
5. Description: "Football odds prediction system"
6. Choose **Public** (or Private if preferred)
7. **⚠️ DO NOT** check "Initialize with README"
8. Click **"Create repository"**

---

### Step 3: Get Your Repository URL

After creating, you'll see this page:
- Look for **"Code"** button (green, top right)
- Copy the HTTPS URL:
  ```
  https://github.com/YOUR_USERNAME/football_odds_predictor.git
  ```

---

### Step 4: Run the Setup Script

Open terminal in your project folder and run:

```bash
cd "c:\Users\DELL\Desktop\Code with Ai\football_odds_predictor"
python setup_github.py
```

**The script will:**
1. ✅ Check Git is installed
2. ✅ Ask for your name and email
3. ✅ Add your GitHub URL
4. ✅ Initialize repository
5. ✅ Stage all files
6. ✅ Create first commit
7. ✅ Push to GitHub
8. ✅ Done! 🎉

---

## Manual Setup (if script doesn't work)

```bash
# Navigate to project
cd "c:\Users\DELL\Desktop\Code with Ai\football_odds_predictor"

# Configure Git (one time)
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# Initialize
git init

# Stage files
git add .

# First commit
git commit -m "Initial commit: Football Odds Predictor with API endpoints"

# Add remote (replace with YOUR URL)
git remote add origin https://github.com/YOUR_USERNAME/football_odds_predictor.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## ✅ Verify It Worked

Visit your GitHub repository URL:
```
https://github.com/YOUR_USERNAME/football_odds_predictor
```

You should see all your files there! ✅

---

## 📝 Future Commits

After setup, use this workflow:

```bash
# Make changes...

# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "git not found" | Restart terminal after installing Git |
| Cannot authenticate | GitHub might ask for password/token first time |
| Files not on GitHub | Make sure you ran `git push` |
| Already using Git | You can skip `git init` |

---

## 💡 Pro Tips

1. **Commit often** - Don't wait until the end
2. **Good messages** - Say what changed and why
3. **Push regularly** - Don't accumulate commits
4. **Use branches** - For new features or experiments

---

**Ready? Install Git and run `setup_github.py`!** 🚀
