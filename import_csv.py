"""
Import Real Matches from CSV File
Get odds from Betpawa/1xbet and save to CSV, then import here
"""

import csv
from app import app, db, OddsRecord
from datetime import datetime

def import_from_csv(csv_file='matches.csv'):
    """
    Import matches from CSV file
    
    CSV Format (with header row):
    home_team,away_team,league,odds_1,odds_x,odds_2,source,is_completed,actual_result,btts,goals_for
    
    Example row:
    Arsenal,Chelsea,Premier League,2.15,3.40,3.50,Betpawa,False,,,
    Man City,Liverpool,Premier League,1.95,3.60,3.80,1xbet,True,1,Y,3
    """
    with app.app_context():
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                added_count = 0
                skipped_count = 0
                
                for row in reader:
                    # Check if match exists
                    existing = OddsRecord.query.filter_by(
                        home_team=row['home_team'],
                        away_team=row['away_team'],
                        league=row['league']
                    ).first()
                    
                    if existing:
                        print(f"⚠️  Skipped (exists): {row['home_team']} vs {row['away_team']}")
                        skipped_count += 1
                        continue
                    
                    # Convert values
                    is_completed = row.get('is_completed', '').lower() == 'true'
                    actual_result = row.get('actual_result') or None
                    btts = row.get('btts') or None
                    goals_for = int(row['goals_for']) if row.get('goals_for') else None
                    
                    match = OddsRecord(
                        match_name=f"{row['home_team']} vs {row['away_team']}",
                        home_team=row['home_team'],
                        away_team=row['away_team'],
                        league=row['league'],
                        odds_1=float(row['odds_1']),
                        odds_x=float(row['odds_x']),
                        odds_2=float(row['odds_2']),
                        source=row['source'],
                        is_completed=is_completed,
                        actual_result=actual_result,
                        btts=btts,
                        goals_for=goals_for,
                        uploaded_at=datetime.now()
                    )
                    
                    db.session.add(match)
                    added_count += 1
                    print(f"✅ Added: {row['home_team']} vs {row['away_team']} ({row['league']})")
                
                db.session.commit()
                
                print("\n" + "=" * 70)
                print(f"✓ Import complete!")
                print(f"  Added: {added_count} matches")
                print(f"  Skipped: {skipped_count} matches (already exist)")
                print("=" * 70)
                
        except FileNotFoundError:
            print(f"❌ Error: File '{csv_file}' not found!")
            print("\nCreate a CSV file with this format:")
            print("home_team,away_team,league,odds_1,odds_x,odds_2,source,is_completed,actual_result,btts,goals_for")
            print("Arsenal,Chelsea,Premier League,2.15,3.40,3.50,Betpawa,False,,,")
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def create_sample_csv():
    """Create a sample CSV template"""
    with open('matches_template.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['home_team', 'away_team', 'league', 'odds_1', 'odds_x', 'odds_2', 
                        'source', 'is_completed', 'actual_result', 'btts', 'goals_for'])
        writer.writerow(['Arsenal', 'Chelsea', 'Premier League', '2.15', '3.40', '3.50', 
                        'Betpawa', 'False', '', '', ''])
        writer.writerow(['Real Madrid', 'Barcelona', 'La Liga', '2.10', '3.30', '3.40', 
                        '1xbet', 'True', '1', 'Y', '3'])
    
    print("✓ Created: matches_template.csv")
    print("  Edit this file and add your real matches, then run:")
    print("  python import_csv.py")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'create-template':
        create_sample_csv()
    else:
        print("=" * 70)
        print("IMPORTING REAL MATCHES FROM CSV")
        print("=" * 70)
        import_from_csv('matches.csv')
