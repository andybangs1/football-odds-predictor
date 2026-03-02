# Deployment Guide - Host for FREE 🚀

## Option 1: Render.com (RECOMMENDED) ⭐

**Best for:** Long-term hosting | Most reliable free tier

### Setup Steps:

1. **Create GitHub Repository**
   ```bash
   cd football_odds_predictor
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub**
   - Create account at github.com
   - Create new repository named "football-odds-predictor"
   - Push your code

3. **Connect to Render**
   - Go to render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select the repository
   - Configure:
     - Name: `football-odds-predictor`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Click Deploy

4. **Install Gunicorn for Production**
   Add to `requirements.txt`:
   ```
   gunicorn==21.2.0
   ```

### Cost: FREE (forever for low-traffic apps)
### Domain: `football-odds-predictor.onrender.com`

---

## Option 2: Replit 🔧

**Best for:** Quick testing | Instant public URL | Free database

### Setup Steps:

1. **Create Replit Account**
   - Go to replit.com
   - Sign in with GitHub/Google

2. **Create New Replit**
   - Click "Create" → "New Repl"
   - Select "Python"
   - Upload your files

3. **Install Dependencies**
   - Click "Packages" icon
   - Install: Flask, Flask-SQLAlchemy, Pillow, pytesseract, numpy

4. **Run**
   - Click "Run" button
   - Your app gets public URL automatically
   - Share the URL

### Cost: FREE
### Domain: Automatic (e.g., `football-odds-predictor.replit.dev`)

---

## Option 3: Heroku (Limited Free) ⚠️

**Best for:** Quick deployment | Legacy platform

### Setup Steps:

1. **Install Heroku CLI**
   - Download from heroku.com/cli

2. **Create Procfile**
   Create file named `Procfile`:
   ```
   web: gunicorn app:app
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### Cost: FREE (550 hours/month - limited)

---

## Option 4: PythonAnywhere

**Best for:** Beginner-friendly | No terminal needed

### Setup Steps:

1. **Create Account**
   - Go to pythonanywhere.com
   - Free account

2. **Upload Files**
   - Use web interface to upload files
   - Or use Git integration

3. **Configure Web App**
   - Add new web app
   - Select Python 3.10
   - Configure WSGI file

4. **Reload**
   - Click "Reload" web app
   - Your URL is ready

### Cost: FREE (limited resources)
### Domain: `username.pythonanywhere.com`

---

## Option 5: Oracle Cloud (Always Free Tier)

**Best for:** More powerful resources | Long-term scaling

### Setup Steps:

1. Create Oracle account (credit card required but free tier doesn't charge)
2. Create Ubuntu VM instance (always free)
3. SSH into instance
4. Clone your repository
5. Install Python and dependencies
6. Run app with `nohup python app.py &`
7. Use reverse proxy (nginx) for public access

### Cost: FREE (genuinely no charges)

---

## Recommended Setup for Maximum Income 💰

**Best combination:**
- **Primary:** Render.com (prod backend)
- **Backup:** Replit (quick testing)

1. Deploy main app on Render for reliability
2. Use Replit for working on new features
3. GitHub as version control
4. Custom domain pointing to Render (optional, paid)

### Your Workflow:
```
Code locally → Git push → GitHub
                            ↓
                       Render deploys automatically
                            ↓
                       Public URL ready to share
```

---

## Making Your URL Social-Media Friendly

### Add Custom Domain (Optional, $1-2/year)

After deploying on Render:
1. Add domain to Render
2. Point domain DNS to Render
3. Share clean URL on Facebook

**With custom domain:**
```
Before: football-odds-predictor-abc123.onrender.com
After:  footballodds.com
```

### Link Shortener (Recommended Free)

Use bit.ly or tinyurl:
```
Link: footballodds.com/predictions
Short: bit.ly/fb-odds-predict
```

---

## Environment Setup for Deployment

Create `.env` file (don't push to GitHub):
```
FLASK_ENV=production
DATABASE_URL=sqlite:///odds_history.db
PYTESSERACT_PATH=/usr/bin/tesseract
```

---

## Monitoring & Updates

1. **Check Logs on Render:**
   - Dashboard → Your App → Logs

2. **Update Code:**
   ```bash
   git push
   # Render auto-deploys
   ```

3. **Database Backup:**
   - Download `odds_history.db` regularly
   - Store locally as backup

---

## Cost Breakdown

| Platform | Cost | Pros | Cons |
|----------|------|------|------|
| **Render** | FREE | Reliable, auto-deploy | Limited CPU |
| **Replit** | FREE | Easy to use, instant URL | Limited uptime |
| **Heroku** | $7/mo | Professional | Limited free tier |
| **PythonAnywhere** | FREE | Beginner-friendly | Limited resources |
| **Oracle Cloud** | FREE | Powerful resources | Complex setup |

---

## Quick Start - Render (60 seconds)

1. Push code to GitHub
2. Go to render.com
3. Connect GitHub → Select repo
4. Deploy (5 mins)
5. Get public URL
6. Share on Facebook

**Total time:** ~10 minutes
**Cost:** $0 forever (for low-traffic apps)

---

## Scaling as You Grow

- **0-100 visits/day:** Free tier works
- **100-1000 visits/day:** Still free, may need cache
- **1000+ visits/day:** Upgrade to paid ($7-25/mo on Render)

By then, affiliate earnings will cover costs 💰

---

## Support

For deployment issues:
- Render: render.com/docs (excellent docs)
- Replit: community.replit.com
- GitHub: GitHub Documentation

Good luck! 🚀
