"""
Reset database with upcoming matches as priority
Most matches will be UPCOMING (is_completed=False)
Only a few recent matches as PAST (is_completed=True)
"""

from app import app, db, OddsRecord
from datetime import datetime

def reset_database():
    """Clear database and reload with proper data (upcoming-focused)"""
    with app.app_context():
        # Delete all existing data
        OddsRecord.query.delete()
        db.session.commit()
        print("✅ Database cleared")
        
        # Add mostly UPCOMING matches with real odds
        upcoming_matches = [
            # ============ UPCOMING MATCHES (MAIN FOCUS) ============
            
            # Premier League Upcoming
            {'home_team': 'Arsenal', 'away_team': 'Liverpool', 'league': 'Premier League',
             'odds_1': 2.25, 'odds_x': 3.40, 'odds_2': 3.10, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Manchester City', 'away_team': 'Chelsea', 'league': 'Premier League',
             'odds_1': 1.80, 'odds_x': 3.80, 'odds_2': 4.20, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Manchester United', 'away_team': 'Tottenham', 'league': 'Premier League',
             'odds_1': 2.10, 'odds_x': 3.50, 'odds_2': 3.40, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Newcastle', 'away_team': 'Brighton', 'league': 'Premier League',
             'odds_1': 1.95, 'odds_x': 3.65, 'odds_2': 3.85, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Aston Villa', 'away_team': 'West Ham', 'league': 'Premier League',
             'odds_1': 2.05, 'odds_x': 3.55, 'odds_2': 3.75, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            
            # La Liga Upcoming
            {'home_team': 'Barcelona', 'away_team': 'Real Madrid', 'league': 'La Liga',
             'odds_1': 2.10, 'odds_x': 3.50, 'odds_2': 3.30, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Atletico Madrid', 'away_team': 'Valencia', 'league': 'La Liga',
             'odds_1': 1.95, 'odds_x': 3.65, 'odds_2': 3.85, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Sevilla', 'away_team': 'Real Betis', 'league': 'La Liga',
             'odds_1': 2.20, 'odds_x': 3.40, 'odds_2': 3.35, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Athletic Bilbao', 'away_team': 'Real Sociedad', 'league': 'La Liga',
             'odds_1': 2.05, 'odds_x': 3.50, 'odds_2': 3.60, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            
            # Serie A Upcoming
            {'home_team': 'Juventus', 'away_team': 'AC Milan', 'league': 'Serie A',
             'odds_1': 2.30, 'odds_x': 3.35, 'odds_2': 3.00, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Inter Milan', 'away_team': 'AS Roma', 'league': 'Serie A',
             'odds_1': 1.70, 'odds_x': 4.00, 'odds_2': 4.80, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Napoli', 'away_team': 'Lazio', 'league': 'Serie A',
             'odds_1': 2.15, 'odds_x': 3.50, 'odds_2': 3.35, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Atalanta', 'away_team': 'Fiorentina', 'league': 'Serie A',
             'odds_1': 1.90, 'odds_x': 3.55, 'odds_2': 4.20, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            
            # Bundesliga Upcoming
            {'home_team': 'Bayern Munich', 'away_team': 'Borussia Dortmund', 'league': 'Bundesliga',
             'odds_1': 1.65, 'odds_x': 4.20, 'odds_2': 5.50, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'RB Leipzig', 'away_team': 'Bayer Leverkusen', 'league': 'Bundesliga',
             'odds_1': 2.20, 'odds_x': 3.50, 'odds_2': 3.25, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'VfB Stuttgart', 'away_team': 'Eintracht Frankfurt', 'league': 'Bundesliga',
             'odds_1': 1.95, 'odds_x': 3.65, 'odds_2': 3.90, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Union Berlin', 'away_team': 'Borussia M\'gladbach', 'league': 'Bundesliga',
             'odds_1': 2.15, 'odds_x': 3.45, 'odds_2': 3.50, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            
            # Ligue 1 Upcoming
            {'home_team': 'PSG', 'away_team': 'Marseille', 'league': 'Ligue 1',
             'odds_1': 1.40, 'odds_x': 5.00, 'odds_2': 9.00, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Monaco', 'away_team': 'Lyon', 'league': 'Ligue 1',
             'odds_1': 2.10, 'odds_x': 3.50, 'odds_2': 3.60, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Lille', 'away_team': 'Nice', 'league': 'Ligue 1',
             'odds_1': 2.05, 'odds_x': 3.30, 'odds_2': 3.75, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Lens', 'away_team': 'Rennes', 'league': 'Ligue 1',
             'odds_1': 2.15, 'odds_x': 3.40, 'odds_2': 3.50, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            
            # Champions League Upcoming
            {'home_team': 'Real Madrid', 'away_team': 'Manchester City', 'league': 'Champions League',
             'odds_1': 2.50, 'odds_x': 3.30, 'odds_2': 2.80, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Bayern Munich', 'away_team': 'Arsenal', 'league': 'Champions League',
             'odds_1': 2.00, 'odds_x': 3.50, 'odds_2': 3.60, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'Inter Milan', 'away_team': 'Atletico Madrid', 'league': 'Champions League',
             'odds_1': 1.95, 'odds_x': 3.60, 'odds_2': 3.80, 'source': 'Betpawa',
             'is_completed': False, 'uploaded_at': datetime.now()},
            {'home_team': 'PSG', 'away_team': 'Barcelona', 'league': 'Champions League',
             'odds_1': 2.40, 'odds_x': 3.35, 'odds_2': 2.85, 'source': '1xbet',
             'is_completed': False, 'uploaded_at': datetime.now()},
            
            # ============ PAST MATCHES (JUST A FEW FOR REFERENCE) ============
            
            {'home_team': 'Liverpool', 'away_team': 'Chelsea', 'league': 'Premier League',
             'odds_1': 2.15, 'odds_x': 3.40, 'odds_2': 3.50, 'actual_result': '1',
             'source': 'Betpawa', 'is_completed': True, 'btts': 'Y', 'goals_for': 3,
             'uploaded_at': datetime.now()},
            {'home_team': 'Real Madrid', 'away_team': 'Barcelona', 'league': 'La Liga',
             'odds_1': 2.00, 'odds_x': 3.60, 'odds_2': 3.40, 'actual_result': 'X',
             'source': '1xbet', 'is_completed': True, 'btts': 'Y', 'goals_for': 2,
             'uploaded_at': datetime.now()},
            {'home_team': 'Inter Milan', 'away_team': 'AC Milan', 'league': 'Serie A',
             'odds_1': 2.10, 'odds_x': 3.30, 'odds_2': 3.50, 'actual_result': '1',
             'source': 'Betpawa', 'is_completed': True, 'btts': 'Y', 'goals_for': 3,
             'uploaded_at': datetime.now()},
            {'home_team': 'Bayern Munich', 'away_team': 'RB Leipzig', 'league': 'Bundesliga',
             'odds_1': 1.75, 'odds_x': 3.80, 'odds_2': 4.80, 'actual_result': '1',
             'source': '1xbet', 'is_completed': True, 'btts': 'Y', 'goals_for': 4,
             'uploaded_at': datetime.now()},
            {'home_team': 'PSG', 'away_team': 'Marseille', 'league': 'Ligue 1',
             'odds_1': 1.45, 'odds_x': 4.80, 'odds_2': 7.50, 'actual_result': '1',
             'source': 'Betpawa', 'is_completed': True, 'btts': 'Y', 'goals_for': 2,
             'uploaded_at': datetime.now()},
        ]
        
        # Add all matches
        for match_data in upcoming_matches:
            match_name = f"{match_data['home_team']} vs {match_data['away_team']}"
            match = OddsRecord(match_name=match_name, **match_data)
            db.session.add(match)
        
        db.session.commit()
        
        # Show stats
        past = OddsRecord.query.filter_by(is_completed=True).count()
        upcoming = OddsRecord.query.filter_by(is_completed=False).count()
        total = past + upcoming
        
        print(f"\n" + "="*70)
        print(f"✅ DATABASE RESET SUCCESSFUL")
        print(f"="*70)
        print(f"📊 Total Matches: {total}")
        print(f"🔴 Past Matches (Completed): {past}")
        print(f"🟢 Upcoming Matches: {upcoming}")
        print(f"="*70)
        print(f"\n✓ Database is now focused on UPCOMING matches!")

if __name__ == '__main__':
    reset_database()
