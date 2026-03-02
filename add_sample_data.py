"""
Add sample past match results for demonstration
This populates the homepage with historical data
"""

from app import app, db, OddsRecord
from datetime import datetime, timedelta

def add_sample_matches():
    with app.app_context():
        # Sample completed matches from top 5 leagues
        sample_matches = [
            {
                'home_team': 'Man City',
                'away_team': 'Arsenal',
                'league': 'Premier League',
                'odds_1': 1.85,
                'odds_x': 3.50,
                'odds_2': 4.20,
                'actual_result': '1',
                'source': 'Betpawa',
                'is_completed': True,
                'btts': 'Y',
                'goals_for': 3,
                'uploaded_at': datetime.now() - timedelta(days=2)
            },
            {
                'home_team': 'Real Madrid',
                'away_team': 'Barcelona',
                'league': 'La Liga',
                'odds_1': 2.10,
                'odds_x': 3.30,
                'odds_2': 3.40,
                'actual_result': 'X',
                'source': '1xbet',
                'is_completed': True,
                'btts': 'Y',
                'goals_for': 2,
                'uploaded_at': datetime.now() - timedelta(days=3)
            },
            {
                'home_team': 'Inter Milan',
                'away_team': 'AC Milan',
                'league': 'Serie A',
                'odds_1': 2.20,
                'odds_x': 3.20,
                'odds_2': 3.25,
                'actual_result': '1',
                'source': 'Betpawa',
                'is_completed': True,
                'btts': 'Y',
                'goals_for': 3,
                'uploaded_at': datetime.now() - timedelta(days=4)
            },
            {
                'home_team': 'Bayern Munich',
                'away_team': 'Dortmund',
                'league': 'Bundesliga',
                'odds_1': 1.65,
                'odds_x': 4.00,
                'odds_2': 5.50,
                'actual_result': '1',
                'source': '1xbet',
                'is_completed': True,
                'btts': 'Y',
                'goals_for': 4,
                'uploaded_at': datetime.now() - timedelta(days=5)
            },
            {
                'home_team': 'PSG',
                'away_team': 'Monaco',
                'league': 'Ligue 1',
                'odds_1': 1.55,
                'odds_x': 4.20,
                'odds_2': 6.00,
                'actual_result': '1',
                'source': 'Betpawa',
                'is_completed': True,
                'btts': 'N',
                'goals_for': 2,
                'uploaded_at': datetime.now() - timedelta(days=6)
            },
            {
                'home_team': 'Liverpool',
                'away_team': 'Chelsea',
                'league': 'Premier League',
                'odds_1': 2.00,
                'odds_x': 3.40,
                'odds_2': 3.75,
                'actual_result': '2',
                'source': '1xbet',
                'is_completed': True,
                'btts': 'Y',
                'goals_for': 3,
                'uploaded_at': datetime.now() - timedelta(days=7)
            },
            {
                'home_team': 'Atletico Madrid',
                'away_team': 'Sevilla',
                'league': 'La Liga',
                'odds_1': 1.90,
                'odds_x': 3.40,
                'odds_2': 4.50,
                'actual_result': 'X',
                'source': 'Betpawa',
                'is_completed': True,
                'btts': 'Y',
                'goals_for': 2,
                'uploaded_at': datetime.now() - timedelta(days=8)
            },
            {
                'home_team': 'Juventus',
                'away_team': 'Napoli',
                'league': 'Serie A',
                'odds_1': 2.30,
                'odds_x': 3.10,
                'odds_2': 3.20,
                'actual_result': '2',
                'source': '1xbet',
                'is_completed': True,
                'btts': 'Y',
                'goals_for': 3,
                'uploaded_at': datetime.now() - timedelta(days=9)
            }
        ]
        
        added_count = 0
        for match_data in sample_matches:
            match_name = f"{match_data['home_team']} vs {match_data['away_team']}"
            
            # Check if match already exists
            existing = OddsRecord.query.filter_by(
                home_team=match_data['home_team'],
                away_team=match_data['away_team']
            ).first()
            
            if not existing:
                match = OddsRecord(
                    match_name=match_name,
                    **match_data
                )
                db.session.add(match)
                added_count += 1
        
        db.session.commit()
        
        print("=" * 50)
        print(f"✓ Added {added_count} sample matches")
        print("=" * 50)
        
        # Show updated stats
        total = OddsRecord.query.count()
        completed = OddsRecord.query.filter_by(is_completed=True).count()
        upcoming = OddsRecord.query.filter_by(is_completed=False).count()
        
        print(f"Total matches: {total}")
        print(f"Completed matches: {completed}")
        print(f"Upcoming matches: {upcoming}")
        print("=" * 50)

if __name__ == '__main__':
    add_sample_matches()
