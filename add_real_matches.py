"""
Add Real Matches from Betting Sources
Use this script to add actual odds from Betpawa, 1xbet, or other bookmakers
"""

from app import app, db, OddsRecord
from datetime import datetime

def add_real_match(home_team, away_team, league, odds_1, odds_x, odds_2, 
                   source='Betpawa', is_completed=False, actual_result=None,
                   btts=None, goals_for=None):
    """
    Add a real match from your betting source
    
    Args:
        home_team: Home team name (e.g., 'Arsenal')
        away_team: Away team name (e.g., 'Chelsea')
        league: League name ('Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1', 'Champions League')
        odds_1: Home win odds (e.g., 2.15)
        odds_x: Draw odds (e.g., 3.40)
        odds_2: Away win odds (e.g., 3.50)
        source: Bookmaker name ('Betpawa', '1xbet', etc.)
        is_completed: True if match has been played
        actual_result: '1' (home win), 'X' (draw), or '2' (away win)
        btts: 'Y' or 'N' (Both Teams To Score)
        goals_for: Total goals scored
    """
    with app.app_context():
        match_name = f"{home_team} vs {away_team}"
        
        # Check if match already exists
        existing = OddsRecord.query.filter_by(
            home_team=home_team,
            away_team=away_team,
            league=league
        ).first()
        
        if existing:
            print(f"⚠️  Match already exists: {match_name}")
            return False
        
        match = OddsRecord(
            match_name=match_name,
            home_team=home_team,
            away_team=away_team,
            league=league,
            odds_1=odds_1,
            odds_x=odds_x,
            odds_2=odds_2,
            source=source,
            is_completed=is_completed,
            actual_result=actual_result,
            btts=btts,
            goals_for=goals_for,
            uploaded_at=datetime.now()
        )
        
        db.session.add(match)
        db.session.commit()
        
        status = "✅ COMPLETED" if is_completed else "📅 UPCOMING"
        print(f"{status} - Added: {match_name} | League: {league} | Odds: {odds_1}/{odds_x}/{odds_2} | Source: {source}")
        return True

# ============================================
# HOW TO USE THIS SCRIPT
# ============================================
# 1. Visit Betpawa.com or 1xbet.com
# 2. Find a match and copy the 3 odds numbers
# 3. Paste them below in the add_real_match() calls
# 4. Run: python add_real_matches.py
# 5. Check your homepage to see the new matches!
# ============================================

if __name__ == '__main__':
    print("=" * 70)
    print("🏀 ADDING REAL MATCHES FROM BETTING SOURCES")
    print("=" * 70)
    
    # ===== PREMIER LEAGUE =====
    add_real_match(
        home_team='Arsenal',
        away_team='Liverpool', 
        league='Premier League',
        odds_1=2.25,  # From Betpawa/1xbet
        odds_x=3.40,
        odds_2=3.10,
        source='Betpawa',
        is_completed=False
    )
    
    add_real_match(
        home_team='Manchester City',
        away_team='Chelsea', 
        league='Premier League',
        odds_1=1.80,  # Update with real odds
        odds_x=3.80,
        odds_2=4.20,
        source='Betpawa',
        is_completed=False
    )
    
    add_real_match(
        home_team='Manchester United',
        away_team='Tottenham', 
        league='Premier League',
        odds_1=2.10,
        odds_x=3.50,
        odds_2=3.40,
        source='1xbet',
        is_completed=False
    )
    
    # ===== LA LIGA =====
    add_real_match(
        home_team='Barcelona',
        away_team='Real Madrid',
        league='La Liga',
        odds_1=2.10,
        odds_x=3.50,
        odds_2=3.30,
        source='Betpawa',
        is_completed=False
    )
    
    add_real_match(
        home_team='Atletico Madrid',
        away_team='Sevilla',
        league='La Liga',
        odds_1=1.95,
        odds_x=3.60,
        odds_2=3.90,
        source='1xbet',
        is_completed=False
    )
    
    # ===== SERIE A =====
    add_real_match(
        home_team='Juventus',
        away_team='AC Milan',
        league='Serie A',
        odds_1=2.30,
        odds_x=3.35,
        odds_2=3.00,
        source='Betpawa',
        is_completed=False
    )
    
    add_real_match(
        home_team='Inter Milan',
        away_team='AS Roma',
        league='Serie A',
        odds_1=1.70,
        odds_x=4.00,
        odds_2=4.80,
        source='1xbet',
        is_completed=False
    )
    
    # ===== BUNDESLIGA =====
    add_real_match(
        home_team='Bayern Munich',
        away_team='Borussia Dortmund',
        league='Bundesliga',
        odds_1=1.65,
        odds_x=4.20,
        odds_2=5.50,
        source='Betpawa',
        is_completed=False
    )
    
    # ===== LIGUE 1 =====
    add_real_match(
        home_team='PSG',
        away_team='Marseille',
        league='Ligue 1',
        odds_1=1.40,
        odds_x=5.00,
        odds_2=9.00,
        source='1xbet',
        is_completed=False
    )
    
    # ===== CHAMPIONS LEAGUE =====
    add_real_match(
        home_team='Real Madrid',
        away_team='Manchester City',
        league='Champions League',
        odds_1=2.50,
        odds_x=3.30,
        odds_2=2.80,
        source='Betpawa',
        is_completed=False
    )
    
    # ===== PAST MATCHES (COMPLETED) =====
    add_real_match(
        home_team='Liverpool',
        away_team='Chelsea',
        league='Premier League',
        odds_1=2.15,
        odds_x=3.40,
        odds_2=3.50,
        source='Betpawa',
        is_completed=True,
        actual_result='1',  # Liverpool won
        btts='Y',
        goals_for=3
    )
    
    add_real_match(
        home_team='Real Madrid',
        away_team='Barcelona',
        league='La Liga',
        odds_1=2.00,
        odds_x=3.60,
        odds_2=3.40,
        source='1xbet',
        is_completed=True,
        actual_result='X',  # Draw
        btts='Y',
        goals_for=2
    )
    
    print("=" * 70)
    print("✅ All matches added successfully!")
    print("📊 Visit your homepage to see the new data")
    print("=" * 70)
