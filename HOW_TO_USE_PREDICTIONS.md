# How to Use the Automatic Prediction System

## ✅ What's Fixed:
1. **Database Updated** - Added columns for team names and match results
2. **Statistics Working** - Now shows completed and pending matches
3. **Automatic Predictions** - System predicts based on historical win percentages
4. **Server Running** - All features now active at http://localhost:5000

---

## 📋 Step-by-Step Guide:

### Step 1: Upload Past Match Results (Build History)
For the system to make accurate predictions, you need to upload past matches with their results first.

1. Go to http://localhost:5000
2. Click **"Upload Odds"** tab
3. Fill in the form:
   - **Match Name**: e.g., "Arsenal vs Chelsea"
   - **Home Team**: e.g., "Arsenal"
   - **Away Team**: e.g., "Chelsea"
   - **Odds 1 (Home Win)**: e.g., 2.50
   - **Odds X (Draw)**: e.g., 3.20
   - **Odds 2 (Away Win)**: e.g., 2.80
   - **Source**: Select "Betpawa" or "1xbet"
   - Upload screenshot (from Desktop or anywhere)
4. Click **Upload**

### Step 2: Mark Match Results
After matches are completed, mark their results:

1. Go to **"History"** tab
2. You'll see all uploaded matches
3. For each completed match, click:
   - **"1"** button = Home team won
   - **"X"** button = Draw
   - **"2"** button = Away team won
4. The match will show a green ✓ badge with the result

### Step 3: Upload New Fixtures for Predictions
Once you have 3+ completed matches with results:

1. Upload a new upcoming match (same as Step 1)
2. **AUTOMATIC PREDICTION** will appear showing:
   - **Recommended Bet**: The outcome with highest win percentage
   - **Win Rates**: Home Win %, Draw %, Away Win %
   - **Team-Specific Analysis**: If these teams played before
   - **Confidence Score**: Based on historical data

### Step 4: View Statistics
1. Click **"Statistics"** tab
2. You'll see:
   - Total uploaded matches
   - Completed vs Pending matches
   - Overall win rates (Home/Draw/Away percentages)
   - Average odds from all matches

---

## 💡 Tips for Best Predictions:

1. **Upload 10-20 past matches first** with known results
2. **Include same teams multiple times** for better team-specific predictions
3. **Mark results promptly** after matches complete
4. **Use consistent team names** (e.g., always "Man United", not "Manchester United" sometimes)
5. **More data = better predictions** - system improves with each completed match

---

## 🎯 What the Predictions Mean:

- **Win Rate %**: Percentage of times that outcome happened in past matches
- **Recommended Bet**: The outcome with the highest historical win rate
- **Confidence Score**: Higher score = more historical data available
- **Team-Specific**: Shows win rates when these exact teams played before

---

## 🔧 If Statistics Still Not Working:

1. Refresh browser with **CTRL + F5** (hard refresh)
2. Make sure server is running (you should see Flask messages in terminal)
3. Upload at least 1 match with a marked result

---

## 📱 Access from Phone:
Your app is accessible on your network at:
- From PC: http://localhost:5000
- From Phone: http://192.168.0.102:5000
(Make sure phone and PC are on same WiFi)

---

## 🚀 Ready to Use!
The system is now fully functional with automatic predictions. Start by uploading past matches and marking their results to build your prediction database!
