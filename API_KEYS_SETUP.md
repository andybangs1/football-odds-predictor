# 🔑 API Keys Setup - Get Real Live Data

Your app now fetches **REAL fixtures from actual web sources** instead of sample data.

## Why You Need API Keys

To get real upcoming matches with actual odds from betting sites and sports databases, you need free API keys from these services.

## 🚀 Quick Setup (5 minutes)

### Option 1: API-Football (RECOMMENDED) ⭐

**Best for:** Real-time fixtures + team names + leagues
**Free tier:** 100 API calls per day

1. Go to: https://www.api-football.com/
2. Click "Get Started" → Sign up (free)
3. Go to Dashboard → Copy your API key
4. Open `fetch_live_fixtures.py`
5. Replace line 15: `API_FOOTBALL_KEY = "YOUR_API_KEY_HERE"`

### Option 2: Football-Data.org

**Best for:** European leagues (Premier League, La Liga, Serie A)
**Free tier:** 10 calls per minute

1. Go to: https://www.football-data.org/client/register
2. Register for free account
3. Check email for API token
4. Open `fetch_live_fixtures.py`
5. Replace line 16: `FOOTBALL_DATA_KEY = "YOUR_TOKEN_HERE"`

### Option 3: The Odds API

**Best for:** Real betting odds from bookmakers
**Free tier:** 500 requests per month

1. Go to: https://the-odds-api.com/
2. Sign up for free account
3. Copy your API key from dashboard
4. Open `fetch_live_fixtures.py`
5. Replace line 17: `ODDS_API_KEY = "YOUR_KEY_HERE"`

### Option 4: TheSportsDB (NO KEY NEEDED)

**Best for:** Free community data (limited)
**Free tier:** Unlimited, no key needed

Already works automatically! No setup required.

## 📝 How to Add Keys

1. Open: `fetch_live_fixtures.py`
2. Find lines 15-17:
   ```python
   API_FOOTBALL_KEY = ""  # Get free key from api-football.com
   FOOTBALL_DATA_KEY = ""  # Get free key from football-data.org
   ODDS_API_KEY = ""  # Get free key from the-odds-api.com
   ```

3. Add your keys:
   ```python
   API_FOOTBALL_KEY = "abc123xyz456"
   FOOTBALL_DATA_KEY = "def789ghi012"
   ODDS_API_KEY = "jkl345mno678"
   ```

4. Save the file

5. Push to GitHub:
   ```bash
   git add fetch_live_fixtures.py
   git commit -m "Add API keys for real data"
   git push origin main
   ```

## ✅ Test Your Setup

Visit your site and it will automatically fetch real matches!

Or run locally:
```bash
python fetch_live_fixtures.py
```

## 🎯 What You'll Get

With API keys configured:
- ✅ Real upcoming matches from tomorrow
- ✅ Actual team names from leagues
- ✅ Real odds from bookmakers
- ✅ Updated automatically on each app restart
- ✅ No more sample/fake data

Without API keys:
- ❌ No fixtures will load
- ⚠️ App will show error message

## 🔒 Security Note

**IMPORTANT:** Your API keys are private!

If you're pushing to public GitHub:
1. Create `.env` file (add to .gitignore)
2. Store keys there instead:
   ```
   API_FOOTBALL_KEY=abc123xyz456
   FOOTBALL_DATA_KEY=def789ghi012
   ```
3. Use `python-dotenv` to load them

For now, you can add keys directly since your repo might be private.

## 📞 Need Help?

If APIs aren't working:
1. Check your API key is correct
2. Verify you haven't exceeded free tier limits
3. Check network/firewall isn't blocking requests
4. Try API-Football first (most reliable)

## 🚀 Deploy

After adding keys locally, push to GitHub and Render will auto-deploy with real data!

```bash
git add fetch_live_fixtures.py
git commit -m "Configure real data sources"
git push origin main
```

Visit: https://football-odds-predictor.onrender.com/refresh-fixtures
