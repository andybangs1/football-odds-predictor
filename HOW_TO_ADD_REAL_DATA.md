# How to Add Real Matches from Betting Sources

## 🎯 You Have 3 Options:

---

## Option 1: Add Matches One by One (Easiest)

1. **Open `add_real_matches.py`**

2. **Go to Betpawa or 1xbet website**
   - Find the match you want
   - Copy the odds (1, X, 2)

3. **Add to the script:**
```python
add_real_match(
    home_team='Arsenal',
    away_team='Chelsea', 
    league='Premier League',
    odds_1=2.15,  # ← Paste home win odds from Betpawa
    odds_x=3.40,  # ← Paste draw odds
    odds_2=3.50,  # ← Paste away win odds
    source='Betpawa',
    is_completed=False  # False = upcoming, True = completed
)
```

4. **Run the script:**
```bash
python add_real_matches.py
```

---

## Option 2: Bulk Import from Excel/CSV

### Step 1: Create CSV Template
```bash
python import_csv.py create-template
```

This creates `matches_template.csv`

### Step 2: Fill with Real Data from Betting Sites

Open in Excel and add your matches:

| home_team | away_team | league | odds_1 | odds_x | odds_2 | source | is_completed | actual_result | btts | goals_for |
|-----------|-----------|--------|--------|--------|--------|--------|--------------|---------------|------|-----------|
| Arsenal | Chelsea | Premier League | 2.15 | 3.40 | 3.50 | Betpawa | False | | | |
| Man City | Liverpool | Premier League | 1.95 | 3.60 | 3.80 | 1xbet | True | 1 | Y | 3 |

### Step 3: Save as `matches.csv` and Import
```bash
python import_csv.py
```

---

## Option 3: Use the Upload Feature (Web Interface)

1. **Visit:** `http://localhost:5000/admin` (or your live URL)

2. **Click "Upload Odds" tab**

3. **Take screenshot of betting slip from Betpawa/1xbet**

4. **Upload** - AI will extract odds automatically!

---

## 📊 Where to Get Real Odds:

### Betpawa
- Website: https://betpawa.com
- Sports → Football → Select league
- Copy odds for each match

### 1xbet
- Website: https://1xbet.com
- Sports → Football → Select competition
- Copy odds (1, X, 2)

### Other Sources:
- Bet365
- Betway
- 22bet
- Any bookmaker you use

---

## 🔄 Updating Match Results:

After a match is played:

**Option A: Via Script**
```python
from app import app, db, OddsRecord

with app.app_context():
    match = OddsRecord.query.filter_by(
        home_team='Arsenal',
        away_team='Chelsea'
    ).first()
    
    if match:
        match.actual_result = '1'  # '1'=home win, 'X'=draw, '2'=away win
        match.is_completed = True
        match.btts = 'Y'  # Both teams scored
        match.goals_for = 3  # Total goals
        db.session.commit()
        print("✓ Result updated!")
```

**Option B: Via Web Interface**
1. Go to `/admin`
2. Click "History" tab
3. Click the winning outcome button (1, X, or 2)

---

## 📝 Quick Start:

```bash
# 1. Run the script to add your first real match
python add_real_matches.py

# 2. Check your homepage
# Visit: http://localhost:5000

# 3. See your real match with odds and predictions!
```

---

## 💡 Tips:

- ✅ Always use odds from **ONE betting site** per match (don't mix sources)
- ✅ Add matches **before they're played** for best predictions
- ✅ Update results **after matches** to improve AI accuracy
- ✅ Use correct league names: 
  - `Premier League`
  - `La Liga`
  - `Serie A`
  - `Bundesliga`
  - `Ligue 1`
  - `Champions League`

---

## 🚀 Deploy Real Data to Live Site:

After adding matches locally:

```bash
# Push to GitHub (triggers Render auto-deploy)
git add instance/odds_history.db
git commit -m "Add real match data"
git push origin main
```

**OR** add matches directly on live site at:
`https://your-site.onrender.com/admin`
