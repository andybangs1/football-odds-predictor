# 🔧 Technical Documentation - Advanced Odds Analysis System

## System Architecture

### Database Schema (Updated)

```sql
OddsRecord Table:
├─ id (INTEGER PRIMARY KEY)                    -- Unique identifier
├─ match_name (VARCHAR(255))                   -- "Arsenal vs Chelsea"
├─ home_team (VARCHAR(100))                    -- "Arsenal"
├─ away_team (VARCHAR(100))                    -- "Chelsea"
├─ odds_1 (FLOAT)                              -- Home win odds (e.g., 2.50)
├─ odds_x (FLOAT)                              -- Draw odds (e.g., 3.40)
├─ odds_2 (FLOAT)                              -- Away win odds (e.g., 2.80)
├─ source (VARCHAR(50))                        -- "Betpawa", "1xbet", etc.
├─ image_path (VARCHAR(255))                   -- Original screenshot path
├─ uploaded_at (DATETIME)                      -- When submitted
├─ actual_result (VARCHAR(1))                  -- '1', 'X', '2', or NULL
├─ is_completed (BOOLEAN)                      -- Match finished?
├─ notes (TEXT)                                -- User notes
├─ btts (VARCHAR(1))                           -- 'Y'/'N' (Both Teams To Score)
└─ goals_for (INTEGER)                         -- Total goals scored

INDICES:
- odds_1, odds_x, odds_2 (for range queries)
- is_completed (for filtering)
- source (for source-specific analysis)
- uploaded_at (for date range queries)
```

---

## Core Functions Overview

### 1. `categorize_odds(odds_value)`

**Purpose:** Place odds into 7 categories for historical matching

**Input:**
```python
categorize_odds(2.50)  # Float odds value
```

**Output:**
```python
{
    'range_name': 'Slight Favorite',
    'min': 2.01,
    'max': 2.50,
    'favorite_type': 'slight_favorite',
    'category_id': 4
}
```

**Categories:**
| ID | Range | Odds | Description |
|-----|-------|------|-------------|
| 1 | Very Heavy Favorite | 1.01-1.30 | -76% implied prob |
| 2 | Heavy Favorite | 1.31-1.60 | -61% implied prob |
| 3 | Favorite | 1.61-2.00 | -50% implied prob |
| 4 | Slight Favorite | 2.01-2.50 | -40% implied prob |
| 5 | Underdog | 2.51-3.50 | -29% implied prob |
| 6 | Heavy Underdog | 3.51-5.00 | -20% implied prob |
| 7 | Extreme Underdog | 5.01-99.99 | <-20% implied prob |

**Algorithm:**
```python
if odds <= 1.30:
    return 'Very Heavy Favorite'
elif odds <= 1.60:
    return 'Heavy Favorite'
# ... etc for all 7 ranges
```

---

### 2. `analyze_odds_range(odds_value, bet_type='1')`

**Purpose:** Find historical matches in same odds range, calculate statistics

**Input:**
```python
analyze_odds_range(odds_value=2.50, bet_type='1')  # Analyze home odds
```

**Output:**
```python
{
    'category': 'Slight Favorite',
    'odds_range': (2.01, 2.50),
    'sample_size': 24,
    'completed_matches': 24,
    'win_rate': 0.625,                    # 62.5%
    'favorite_rate': 0.625,               # How often favorite wins
    'underdog_rate': 0.167,               # How often underdog wins
    'btts_rate': 0.542,                   # 54.2% both teams scored
    'draw_rate': 0.208,                   # 20.8% draws
    'confidence': 85,                     # How confident (0-100)
    'matches_in_range': [...]             # List of matching historical records
}
```

**SQL Query Logic:**
```sql
SELECT * FROM odds_record 
WHERE 
  is_completed = TRUE AND
  odds_1 BETWEEN 2.01 AND 2.50 AND  -- Odds range
  actual_result IS NOT NULL           -- Has result
ORDER BY uploaded_at DESC
LIMIT 100
```

**Confidence Calculation:**
```python
# Based on sample size
if sample_size >= 50:
    confidence = 95
elif sample_size >= 30:
    confidence = 85
elif sample_size >= 15:
    confidence = 70
elif sample_size >= 5:
    confidence = 50
else:
    confidence = 20  # Very low confidence
```

**Win Rate Calculation:**
```python
# For bet_type='1' (home odds)
home_wins = count(actual_result == '1')
win_rate = home_wins / total_matches

# For bet_type='X' (draw odds)
draws = count(actual_result == 'X')
win_rate = draws / total_matches

# For bet_type='2' (away odds)
away_wins = count(actual_result == '2')
win_rate = away_wins / total_matches
```

---

### 3. `calculate_implied_probability(odds)`

**Purpose:** Convert decimal odds to implied win probability

**Input:**
```python
calculate_implied_probability(2.50)  # Decimal odds
```

**Output:**
```python
0.40  # 40% implied probability
```

**Formula:**
```python
implied_prob = 1.0 / odds

# Examples:
1.50 odds → 1/1.50 = 0.667 = 66.7%
2.00 odds → 1/2.00 = 0.500 = 50.0%
3.00 odds → 1/3.00 = 0.333 = 33.3%
```

**Note:** This assumes no house margin. Real implied probs are slightly lower (bookmakers profit margin).

---

### 4. `is_value_bet(win_rate, implied_prob, margin=5)`

**Purpose:** Detect if a bet has positive value

**Input:**
```python
is_value_bet(
    win_rate=0.625,        # 62.5% from historical analysis
    implied_prob=0.40,     # 40% from 2.50 odds
    margin=5               # 5% minimum edge (default)
)
```

**Output:**
```python
True  # This is a value bet!
```

**Logic:**
```python
edge_percent = (win_rate - implied_prob) * 100
value_exists = edge_percent > margin

# Example:
# (0.625 - 0.40) * 100 = 22.5% edge
# 22.5% > 5% minimum ✓ VALUE FOUND!
```

**Value Classification:**
```python
edge_percent = (win_rate - implied_prob) * 100

if edge_percent > 15:
    value_rating = "EXCELLENT"  # 💎💎💎
elif edge_percent > 10:
    value_rating = "GOOD"       # 💎💎
elif edge_percent > 5:
    value_rating = "OKAY"       # 💎
else:
    value_rating = "NO_VALUE"   # ❌
```

---

### 5. `generate_prediction(home_team, away_team, odds_1, odds_x, odds_2, source)`

**Purpose:** Comprehensive prediction with all analysis

**Input:**
```python
generate_prediction(
    home_team='Arsenal',
    away_team='Chelsea',
    odds_1=2.50,
    odds_x=3.40,
    odds_2=2.80,
    source='Betpawa'
)
```

**Output:**
```python
{
    'match': 'Arsenal vs Chelsea',
    'date': '2024-02-24',
    'source': 'Betpawa',
    
    # Analysis for each outcome
    'analysis': {
        '1': {                            # Home win
            'odds': 2.50,
            'implied_prob': 0.40,
            'win_rate': 0.625,
            'confidence': 85,
            'is_value_bet': True,
            'value_edge': 22.5,           # Percentage
            'rationale': "Heavy historical backing at this odds level"
        },
        'X': {                            # Draw
            'odds': 3.40,
            'implied_prob': 0.294,
            'win_rate': 0.208,
            'confidence': 70,
            'is_value_bet': False,
            'value_edge': -8.6,
            'rationale': "Below historical frequency for this range"
        },
        '2': {                            # Away win
            'odds': 2.80,
            'implied_prob': 0.357,
            'win_rate': 0.415,
            'confidence': 75,
            'is_value_bet': False,
            'value_edge': 5.8,
            'rationale': "Slight value but confidence lower"
        }
    },
    
    # Best recommendation
    'best_prediction': '1',         # Home win
    'best_odds': 2.50,
    'best_win_rate': 0.625,
    'best_confidence': 85,
    'best_rationale': "Arsenal favored historically at 2.01-2.50 odds",
    
    # Value betting
    'has_value_bets': True,
    'value_bets': [
        {
            'outcome': '1',
            'odds': 2.50,
            'edge': 22.5,
            'rating': 'EXCELLENT'
        }
    ],
    
    # Additional statistics
    'btts_rate': 0.542,             # 54.2% both teams score
    'average_confidence': 76,
    'recommendation': "BET HOME WIN @ 2.50 - Excellent value, high confidence"
}
```

**Decision Tree:**
```python
1. Analyze all three outcomes (1, X, 2)
2. Calculate win_rate and value_edge for each
3. Find best prediction and best value bet
4. Return comprehensive recommendation
5. Flag if multiple value opportunities exist
```

---

## API Endpoints

### 1. POST `/odds-analysis`

**Purpose:** Analyze odds and detect value

**Request:**
```json
{
    "odds_1": 2.50,
    "odds_x": 3.40,
    "odds_2": 2.80,
    "home_team": "Arsenal",
    "away_team": "Chelsea",
    "source": "Betpawa"
}
```

**Response:**
```json
{
    "status": "success",
    "prediction": {
        "match": "Arsenal vs Chelsea",
        "best_prediction": "1",
        "best_odds": 2.50,
        "win_rate": 62.5,
        "has_value_bets": true,
        "value_edge": 22.5,
        "confidence": 85
    }
}
```

**Error Response:**
```json
{
    "status": "error",
    "message": "Not enough historical data for analysis",
    "minimum_matches_needed": 5,
    "matches_found": 2
}
```

---

### 2. POST `/update-btts/<record_id>`

**Purpose:** Record BTTS result and goals

**Request:**
```json
{
    "btts": "Y",           // "Y" or "N"
    "goals_for": 3         // Total goals in match
}
```

**Response:**
```json
{
    "status": "success",
    "message": "BTTS updated successfully",
    "record_id": 42,
    "btts": "Y",
    "goals_for": 3
}
```

**Database Update:**
```sql
UPDATE odds_record 
SET btts = 'Y', goals_for = 3 
WHERE id = 42
```

---

### 3. GET `/value-bets`

**Purpose:** List all detected value betting opportunities

**Query Parameters:**
```
?source=Betpawa          // Optional: filter by source
?min_confidence=80       // Optional: minimum confidence level
?min_edge=10             // Optional: minimum value edge %
```

**Response:**
```json
{
    "status": "success",
    "total_matches": 156,
    "value_bets_found": 23,
    "value_bets": [
        {
            "id": 42,
            "match": "Arsenal vs Chelsea",
            "odds": 2.50,
            "outcome": "1",
            "win_rate": 62.5,
            "implied_prob": 40.0,
            "edge": 22.5,
            "confidence": 85,
            "source": "Betpawa",
            "uploaded_at": "2024-02-24"
        },
        {
            "id": 43,
            "match": "Man City vs Liverpool",
            "odds": 1.95,
            "outcome": "1",
            "win_rate": 71.0,
            "implied_prob": 51.3,
            "edge": 19.7,
            "confidence": 80,
            "source": "1xbet",
            "uploaded_at": "2024-02-24"
        }
        // ... more value bets
    ],
    "summary": {
        "best_edge": 22.5,
        "average_edge": 12.3,
        "best_confidence": 95,
        "average_confidence": 78
    }
}
```

---

### 4. GET `/odds-report`

**Purpose:** Generate comprehensive analysis table

**Query Parameters:**
```
?source=Betpawa          // Optional: filter by source
?min_confidence=70       // Optional: minimum confidence
```

**Response:**
```json
{
    "status": "success",
    "generated_at": "2024-02-24T14:30:00",
    "total_matches": 156,
    "matches_analyzed": 156,
    "value_bets_found": 23,
    
    "report": [
        {
            "match_id": 42,
            "match": "Arsenal vs Chelsea",
            "status": "completed",
            "odds_display": "2.50 / 3.40 / 2.80",
            "prediction": "Home Win @ 2.50",
            "win_rate_percent": 62.5,
            "btts_percent": 54.2,
            "confidence_percent": 85,
            "is_value_bet": true,
            "value_edge": 22.5,
            "rationale": "Strong historical backing for 2.01-2.50 range | VALUE BET: +22.5% edge"
        },
        {
            "match_id": 43,
            "match": "Man City vs Liverpool",
            "status": "pending",
            "odds_display": "1.95 / 3.60 / 3.40",
            "prediction": "Home Draw @ 3.60",
            "win_rate_percent": 55.0,
            "btts_percent": 68.0,
            "confidence_percent": 75,
            "is_value_bet": false,
            "value_edge": 0,
            "rationale": "Slight favorite pattern expected"
        }
        // ... more matches
    ],
    
    "summary": {
        "total_matches": 156,
        "completed_matches": 142,
        "pending_matches": 14,
        "value_bets_found": 23,
        "average_confidence": 78,
        "high_confidence_count": 87,  // 80%+ confidence
        "best_value_edge": 22.5
    }
}
```

---

## Frontend JavaScript Functions

### `loadOddsReport()`

**Purpose:** Fetch odds report data and render table

**Flow:**
```javascript
1. GET /odds-report?source=selectedSource
2. Receive JSON with match data
3. Build HTML table rows
4. Highlight value bets (yellow background)
5. Display status badges
6. Insert into DOM
```

**Table HTML Structure:**
```html
<table class="odds-report-table">
  <thead>
    <tr>
      <th>Match</th>
      <th>Status</th>
      <th>Odds (1/X/2)</th>
      <th>Prediction</th>
      <th>Win %</th>
      <th>BTTS %</th>
      <th>Confidence</th>
      <th>Rationale</th>
    </tr>
  </thead>
  <tbody>
    <!-- Rows populated by JavaScript -->
  </tbody>
</table>
```

**Value Bet Row Styling:**
```css
.value-bet-row {
    background: linear-gradient(90deg, rgba(255,193,7,0.15) 0%, transparent 100%);
    border-left: 3px solid #FFC107;
}
```

---

## Database Query Patterns

### Pattern 1: Historical Analysis Query

```sql
-- Find all completed matches with Home odds in range
SELECT 
    id, match_name, home_team, away_team,
    odds_1, actual_result, btts, goals_for,
    uploaded_at
FROM odds_record
WHERE 
    is_completed = TRUE
    AND odds_1 >= 2.01 AND odds_1 <= 2.50
    AND actual_result IS NOT NULL
    AND source = 'Betpawa'  -- Optional source filter
ORDER BY uploaded_at DESC
LIMIT 100;
```

### Pattern 2: BTTS Frequency Query

```sql
-- Calculate BTTS rate for odds range
SELECT 
    COUNT(*) as total_matches,
    SUM(CASE WHEN btts = 'Y' THEN 1 ELSE 0 END) as btts_count,
    ROUND(
        100.0 * SUM(CASE WHEN btts = 'Y' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) as btts_percent
FROM odds_record
WHERE 
    is_completed = TRUE
    AND odds_1 >= 2.01 AND odds_1 <= 2.50
    AND btts IS NOT NULL;
```

### Pattern 3: Win Rate Query

```sql
-- Calculate win rate by outcome
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN actual_result = '1' THEN 1 ELSE 0 END) as home_wins,
    SUM(CASE WHEN actual_result = 'X' THEN 1 ELSE 0 END) as draws,
    SUM(CASE WHEN actual_result = '2' THEN 1 ELSE 0 END) as away_wins,
    ROUND(100.0 * SUM(CASE WHEN actual_result = '1' THEN 1 ELSE 0 END) / COUNT(*), 1) as win_rate
FROM odds_record
WHERE 
    is_completed = TRUE
    AND odds_1 >= 2.01 AND odds_1 <= 2.50;
```

---

## Error Handling

### Common Errors and Responses

| Error | Cause | Response | Solution |
|-------|-------|----------|----------|
| Not enough data | <5 historical matches | {status: error, min_matches: 5, found: 2} | Upload more historical data |
| Invalid odds | odds_1 = 0 or negative | {status: error, message: "Invalid odds"} | Verify odds values |
| Database error | Connection failed | {status: error, message: "DB error"} | Check database connection |
| Missing result | actual_result = NULL | Match excluded from analysis | Mark result when complete |

---

## Performance Optimization

### Query Optimization:
```python
# GOOD: Use indexed columns
WHERE is_completed = TRUE AND odds_1 BETWEEN 2.01 AND 2.50

# BAD: Full table scan
WHERE CAST(odds_1 AS VARCHAR) LIKE '2.%'
```

### Caching Strategy:
```python
# Cache odds report for 5 minutes
CACHE_DURATION = 300
cache[report_key] = data
```

### Batch Processing:
```python
# Process multiple matches in one query
matches = db.query().filter(is_completed=True).limit(100)
```

---

## Testing Checklist

### Unit Tests:
- [ ] categorize_odds() with edge values (1.30, 2.50, 5.00)
- [ ] analyze_odds_range() with 0 matches, 5 matches, 100+ matches
- [ ] calculate_implied_probability() for 1.50, 2.00, 3.00
- [ ] is_value_bet() with edge = 0%, 5%, 10%, 20%
- [ ] generate_prediction() returns all required fields

### Integration Tests:
- [ ] Upload match → Mark result → Analyze in report
- [ ] Multiple matches → Filter by source → Verify count
- [ ] Value bets → Sort by edge → Top value displayed
- [ ] Confidence calculation → 5 matches = 50%, 50 matches = 95%

### UI Tests:
- [ ] Table renders with data
- [ ] Value bet highlighting visible (yellow)
- [ ] Status badges show correctly
- [ ] Source filter works
- [ ] Confidence bars display

---

## Migration History

### Migration 1: Add BTTS Columns
```python
# migrate_btts.py
ALTER TABLE odds_record ADD COLUMN btts VARCHAR(1);
ALTER TABLE odds_record ADD COLUMN goals_for INTEGER;

# Result: Table now has 15 columns
```

---

## Code Statistics

| Component | Files | Lines | Purpose |
|-----------|-------|-------|---------|
| Database Model | app.py | 20 | 15-column OddsRecord |
| Analysis Functions | app.py | 200+ | Odds categorization, prediction, value detection |
| API Endpoints | app.py | 240+ | 4 new REST endpoints |
| Frontend Table | index.html | 30 | Analysis tab structure |
| JavaScript Logic | script.js | 130+ | Table generation, filtering, highlighting |
| Database Migration | migrate_btts.py | 40 | Schema updates |

**Total New Code: ~660 lines**

---

**For questions about specific functions, see inline code comments in app.py**
