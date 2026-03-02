# System Architecture & How It Works

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR FACEBOOK (5K+ followers)            │
│  Posts daily predictions with affiliate links               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│        Football Odds Predictor Web App (Your Tool)          │
│  URL: yourapp.onrender.com or localhost:5000               │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Frontend (HTML/CSS/JavaScript)           │    │
│  │  - Upload page (drag & drop)                       │    │
│  │  - History view (all odds)                         │    │
│  │  - Predictions (AI analysis)                       │    │
│  │  - Statistics (analytics)                          │    │
│  └────────────────────────────────────────────────────┘    │
│                         ↕                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │          Backend (Flask Python App)                │    │
│  │  - API endpoints (/upload, /predict, etc)         │    │
│  │  - OCR image processing (extract odds)            │    │
│  │  - Prediction algorithm                           │    │
│  │  - Data validation                                │    │
│  └────────────────────────────────────────────────────┘    │
│                         ↕                                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │    Database (SQLite - no setup needed)             │    │
│  │  - Match records                                   │    │
│  │  - Odds history                                    │    │
│  │  - Uploaded screenshots                           │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
        ↓                                        ↓
   Your User              Affiliate Networks (Bet365, 1xbet, etc)
   (Follower)             - Track signups
   - Clicks link          - Calculate commissions
   - Signs up             - Process payouts
   - Places bets          → You earn money! 💰
```

## User Journey

### Step 1: Data Collection
```
You take screenshot of Betpawa/1xbet odds
        ↓
Upload to app with match name
        ↓
App extracts numbers (OCR)
        ↓
Save to database with timestamp
```

### Step 2: Analysis
```
User requests prediction
        ↓
App retrieves last 20 odds records
        ↓
Calculate moving average
        ↓
Detect trend (UP/DOWN)
        ↓
Calculate confidence score
        ↓
Return prediction to user
```

### Step 3: Social Media Sharing
```
Copy prediction
        ↓
Post to Facebook + Affiliate Link
        ↓
Followers see prediction
        ↓
Some click your affiliate link
        ↓
They sign up
        ↓
You earn commission! 💰
```

## Component Interactions

```
┌──────────────────┐
│  Browser/Phone   │
│  (User opens app)│
└────────┬─────────┘
         │ HTTP Request
         ↓
   ┌─────────────┐
   │   Flask     │
   │   Server    │
   └────┬────────┘
        │
        ├─→ File uploaded
        │   ├─→ Save to disk
        │   ├─→ Run OCR
        │   └─→ Extract odds
        │
        ├─→ Request prediction
        │   ├─→ Query database
        │   ├─→ Analyze trends
        │   └─→ Generate prediction
        │
        ├─→ View history
        │   ├─→ Query all records
        │   └─→ Format JSON
        │
        └─→ Get statistics
            ├─→ Count records
            ├─→ Calculate averages
            └─→ Format response
             
        ↓ Database
   ┌──────────────────┐
   │   SQLite DB      │
   │  - Records       │
   │  - Photos        │
   │  - Predictions   │
   └──────────────────┘
```

## Prediction Algorithm (Simplified)

```
INPUT: Current odds for a match
┌─────────────────────────────┐
│  Historical Data:           │
│  - Match 1: 2.50, 3.20, 2.80│
│  - Match 2: 2.48, 3.18, 2.85│
│  - Match 3: 2.45, 3.25, 2.90│
│  - ... (up to 20 records)   │
└─────────────────────────────┘
         ↓
┌─────────────────────────────┐
│  Step 1: Extract home odds  │
│  (Home, Draw, Away)         │
│  [2.50, 3.20, 2.80]         │
└─────────────────────────────┘
         ↓
┌─────────────────────────────┐
│  Step 2: Calculate average  │
│  of last 3 records          │
│  Avg = (2.50 + 2.48 + 2.45) │
│      / 3 = 2.48             │
└─────────────────────────────┘
         ↓
┌─────────────────────────────┐
│  Step 3: Compare current    │
│  vs predicted               │
│  Current: 2.50              │
│  Predicted: 2.48            │
│  Trend: DOWN ⬇️             │
└─────────────────────────────┘
         ↓
┌─────────────────────────────┐
│  Step 4: Confidence score   │
│  = records_count × 10       │
│  = 20 × 10 = 200% → 95%     │
│  (capped at 95%)            │
└─────────────────────────────┘
         ↓
OUTPUT: Next odds prediction with confidence
```

## Technology Stack

```
Frontend Layer:
├─ HTML5 (structure)
├─ CSS3 (beautiful design)
└─ JavaScript (interactivity)

Application Layer:
└─ Flask (Python web framework)
   ├─ File upload handling
   ├─ API endpoints
   └─ Business logic

Data Processing Layer:
├─ Pillow (image processing)
├─ Pytesseract (OCR - optional)
└─ NumPy (data analysis)

Data Layer:
└─ SQLite (embedded database)
   └─ SQLAlchemy (ORM)

Hosting Layer (when deployed):
├─ Render.com (recommended)
├─ Replit
├─ Oracle Cloud
└─ Other options
```

## Database Schema Visualization

```
┌─────────────────────────────────────┐
│        OddsRecord Table              │
├─────────────────────────────────────┤
│ id (integer) - unique identifier   │
│ match_name (text) - "Villa vs City" │
│ odds_1 (float) - home win = 2.50   │
│ odds_x (float) - draw = 3.20       │
│ odds_2 (float) - away win = 2.80   │
│ source (text) - "Betpawa"/"1xbet"  │
│ image_path (text) - screenshot.jpg │
│ uploaded_at (datetime) - timestamp │
│ notes (text) - user notes          │
└─────────────────────────────────────┘

Relationships:
- One app can have many records
- Records sorted by uploaded_at
- Source used for prediction grouping
```

## File System Structure

```
football_odds_predictor/
│
├─ Code Files (Python/Web)
│  ├── app.py (900 lines - backend)
│  ├── templates/index.html (500 lines - webpage)
│  ├── static/style.css (400 lines - design)
│  └── static/script.js (300 lines - logic)
│
├─ Configuration
│  ├── requirements.txt (dependencies)
│  ├── run.bat (Windows launcher)
│  └── run.sh (Mac/Linux launcher)
│
├─ Documentation
│  ├── README.md (full guide)
│  ├── QUICKSTART.md (5 min start)
│  ├── DEPLOYMENT.md (free hosting)
│  ├── MONETIZATION.md (make money)
│  └── PROJECT_SUMMARY.md (this overview)
│
└─ Data (created at runtime)
   ├── uploads/ (images)
   └── odds_history.db (database)
```

## API Endpoints

```
POST /upload
├─ Input: Image file + match details
├─ Processing:
│  ├─ Save image to uploads/
│  ├─ Extract odds with OCR
│  ├─ Validate data
│  └─ Insert into database
└─ Output: JSON with extracted data

GET /history?limit=20
├─ Processing:
│  ├─ Query database (last 20 records)
│  ├─ Format JSON
│  └─ Return data
└─ Output: Array of odds records

GET /predict/<match_id>
├─ Input: Match ID
├─ Processing:
│  ├─ Get match details
│  ├─ Fetch historical data
│  ├─ Run prediction algorithm
│  └─ Calculate confidence
└─ Output: JSON with prediction

GET /stats
├─ Processing:
│  ├─ Count total records
│  ├─ Count by source
│  ├─ Calculate averages
│  └─ Format response
└─ Output: JSON with statistics

DELETE /delete/<record_id>
├─ Processing:
│  ├─ Delete from database
│  ├─ Delete image file
│  └─ Return confirmation
└─ Output: Success message

GET /image/<filename>
├─ Processing: Stream file
└─ Output: Image file (displayed in browser)
```

## Performance Flow

```
User Action          Time    Processing
─────────────────────────────────────────
1. Takes screenshot   1s     (manual)
2. Uploads image      2s     - Upload 1s
                              - Process 1s
3. Saves to DB        <100ms  - Insert
4. View history       <200ms  - Query
5. Get prediction     <500ms  - Calculate
6. Show stats         <300ms  - Aggregate
```

## Security Architecture

```
Input Validation
├─ File type check (jpg/png only)
├─ File size limit (16MB max)
├─ Filename sanitization
└─ Path traversal prevention

Database Security
├─ SQL injection protection (ORM)
├─ Parameterized queries
└─ No raw SQL

API Security
├─ CORS ready (add if needed)
├─ Rate limiting (can add)
├─ Request validation
└─ Error handling

Data Privacy
├─ All data stored locally
├─ No third-party tracking
├─ User controls their data
└─ Optional cloud backup
```

## Deployment Architecture

```
Local Development:
Your Computer → localhost:5000 → Flask → SQLite

Production (Free Tier):
┌──────────────────────────────┐
│    Internet Users            │
│  (Your Facebook followers)   │
└────────────┬─────────────────┘
             │ HTTPS
             ↓
    ┌─────────────────────┐
    │   Render.com        │
    │  (Web Server)       │
    └─────┬───────────────┘
          │
┌─────────┴──────────────┐
│                        │
↓                        ↓
Flask App           Static Files
(app.py)            (CSS, JS, HTML)
    │
    ↓
SQLite Database
(odds_history.db)
```

## Scaling Path

```
Phase 1 (Week 1-2): Hobby
├─ 1-5 predictions/day
├─ 5k Facebook followers
└─ 0 revenue (building audience)

Phase 2 (Week 3-4): Monetization
├─ 5-10 predictions/day
├─ Affiliate links active
├─ 10-20 daily clicks
└─ $50-500/month

Phase 3 (Month 2): Growth
├─ 10-20 predictions/day
├─ 100+ daily clicks
├─ 50 affiliate signups
└─ $1,500-3,000/month

Phase 4 (Month 3+): Scale
├─ Multi-platform (Instagram, TikTok)
├─ Premium subscription tier
├─ 500+ daily clicks
└─ $5,000-10,000+/month
```

## Success Metrics Dashboard

```
Daily Metrics:
├─ Predictions uploaded: _____ (goal: 5-10)
├─ Facebook posts: _____ (goal: 3+)
├─ Engagement rate: ____% (goal: 5%+)
└─ Website visits: ______ (goal: 50+)

Weekly Metrics:
├─ Total predictions: _____ (goal: 35+)
├─ Affiliate clicks: ______ (goal: 50+)
├─ New followers gained: ____ (goal: 50+)
└─ Revenue: $_______ (goal: $100+)

Monthly Metrics:
├─ Total records: _______ (goal: 150+)
├─ Affiliate signups: ____ (goal: 20+)
├─ Accuracy rate: ____% (goal: 75%+)
└─ Revenue: $_______ (goal: $500+)
```

---

## Simple Version: How Money Flows

```
You → Upload Odds → Share on Facebook → Users Click Link → Sign Up
                                            ↓
                                        Bet365/1xbet
                                            ↓
                                    User deposits & bets
                                            ↓
                                    30-40% commission paid to you
                                            ↓
                                        💰 MONEY IN YOUR POCKET
```

---

## Quick Reference

| Aspect | Details |
|--------|---------|
| **Setup Time** | 5 minutes |
| **Tech Stack** | Flask, SQLite, JavaScript |
| **Database** | 0 setup (embedded SQLite) |
| **Hosting** | Free forever (Render.com) |
| **Users** | Your 5k Facebook followers |
| **Revenue Model** | Affiliate commissions |
| **Scale** | $500-10,000/month potential |
| **Time to First $100** | ~2 weeks |
| **Time to $1000/month** | ~6 weeks |

---

You now understand the complete system! 🎯

Ready to launch? See QUICKSTART.md
