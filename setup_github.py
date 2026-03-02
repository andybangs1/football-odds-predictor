#!/usr/bin/env python
"""
GitHub Setup Helper - Interactive script to connect project to GitHub
Run this after installing Git and creating a GitHub repository
"""

import os
import subprocess
import sys

def run_command(cmd, description=""):
    """Run a shell command and return success/failure"""
    try:
        if description:
            print(f"\n▶ {description}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            if description:
                print(f"  ✅ Success")
            return True
        else:
            print(f"  ❌ Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("GitHub Setup Helper - Football Odds Predictor")
    print("=" * 60)
    
    # Check if Git is installed
    print("\n1️⃣  Checking Git installation...")
    if not run_command("git --version"):
        print("\n❌ Git is not installed!")
        print("Download from: https://git-scm.com/downloads")
        print("Then run this script again.")
        sys.exit(1)
    
    git_version = subprocess.run("git --version", shell=True, capture_output=True, text=True).stdout.strip()
    print(f"   ✅ Found: {git_version}")
    
    # Get user info
    print("\n2️⃣  Configure Git User")
    name = input("   Enter your name: ").strip()
    email = input("   Enter your email: ").strip()
    
    if not name or not email:
        print("   ❌ Name and email are required")
        sys.exit(1)
    
    run_command(f'git config --global user.name "{name}"', "Setting Git username")
    run_command(f'git config --global user.email "{email}"', "Setting Git email")
    
    # Get GitHub URL
    print("\n3️⃣  GitHub Repository Connection")
    print("   Go to GitHub.com and create a new repository")
    print("   Repository name: football_odds_predictor")
    print("   DO NOT initialize with README (your files are already there)")
    
    github_url = input("\n   Enter your GitHub repo URL (e.g., https://github.com/username/football_odds_predictor.git): ").strip()
    
    if not github_url:
        print("   ❌ GitHub URL is required")
        sys.exit(1)
    
    # Navigate to project
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"\n4️⃣  Working directory: {project_dir}")
    
    # Initialize Git
    if not os.path.exists(".git"):
        print("\n5️⃣  Initializing Git repository...")
        run_command("git init", "Initializing repository")
    else:
        print("\n5️⃣  Repository already initialized")
    
    # Create .gitignore
    print("\n6️⃣  Creating .gitignore...")
    gitignore_content = """# Python
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
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("   ✅ .gitignore created")
    
    # Add files
    print("\n7️⃣  Adding files to Git...")
    run_command("git add .", "Staging all files")
    
    # Commit
    print("\n8️⃣  Creating initial commit...")
    run_command(
        'git commit -m "Initial commit: Football Odds Predictor with API endpoints"',
        "Creating commit"
    )
    
    # Add remote
    print("\n9️⃣  Connecting to GitHub...")
    # First check if remote exists
    result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("   ⚠️  Remote already exists, skipping...")
    else:
        run_command(f'git remote add origin {github_url}', "Adding remote repository")
    
    # Set branch
    print("\n🔟 Setting main branch...")
    run_command("git branch -M main", "Renaming to main branch")
    
    # Push
    print("\n1️⃣1️⃣  Pushing to GitHub...")
    if run_command("git push -u origin main", "Pushing files"):
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Project is now on GitHub!")
        print("=" * 60)
        print(f"\nFuture commits:")
        print("  git add .")
        print("  git commit -m 'Your message'")
        print("  git push")
        print("\nVisit your repo: " + github_url.replace(".git", ""))
    else:
        print("\n⚠️  Push failed. This might be due to authentication.")
        print("   Make sure:")
        print("   1. Your GitHub URL is correct")
        print("   2. You have credentials saved (GitHub will prompt)")
        print("   3. Personal Access Token is active (for HTTPS)")
        print("\nManual push command:")
        print("  git push -u origin main")

if __name__ == "__main__":
    main()
