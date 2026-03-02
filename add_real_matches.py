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
# ADD YOUR REAL MATCHES HERE
# ============================================

if __name__ == '__main__':
    print("=" * 70)
    print("ADDING REAL MATCHES FROM BETTING SOURCES")
    print("=" * 70)
    
    # Example: Add upcoming match from Betpawa
    # Copy odds directly from the betting site
    
    # PREMIER LEAGUE - UPCOMING (Change these to real odds from your source)
    add_real_match(
        home_team='Arsenal',
        away_team='Liverpool', 
        league='Premier League',
        odds_1=2.25,  # Home win odds from Betpawa
        odds_x=3.40,  # Draw odds
        odds_2=3.10,  # Away win odds
        source='Betpawa',
        is_completed=False  # Upcoming match
    )
    
    # LA LIGA - UPCOMING
    add_real_match(
        home_team='Barcelona',
        away_team='Real Madrid',
        league='La Liga',
        odds_1=2.10,  # Real odds from 1xbet
        odds_x=3.50,
        odds_2=3.30,
        source='1xbet',
        is_completed=False
    )
    
    # Example: Add completed match with result
    add_real_match(
        home_team='Man City',
        away_team='Tottenham',
        league='Premier League',
        odds_1=1.45,
        odds_x=4.80,
        odds_2=7.50,
        source='Betpawa',
        is_completed=True,      # Match completed
        actual_result='1',      # Home team won
        btts='Y',              # Both teams scored
        goals_for=3            # Total 3 goals
    )
    
    # ADD MORE MATCHES BELOW - Copy/paste the template above
    # Just change the team names, league, and odds from your betting source
    
    print("=" * 70)
    print("✓ Done! Visit your homepage to see the matches")
    print("=" * 70)
