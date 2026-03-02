from app import app, db, OddsRecord

with app.app_context():
    total = OddsRecord.query.count()
    completed = OddsRecord.query.filter_by(is_completed=True).count()
    upcoming = OddsRecord.query.filter_by(is_completed=False).count()
    
    print("=" * 50)
    print("DATABASE STATUS")
    print("=" * 50)
    print(f"Total matches: {total}")
    print(f"Completed matches: {completed}")
    print(f"Upcoming matches: {upcoming}")
    print("=" * 50)
