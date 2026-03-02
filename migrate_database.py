"""
Database Migration Script
Adds new columns to existing database for prediction features
"""
import sqlite3
import os

def migrate_database():
    """Add new columns to odds_history table"""
    db_path = os.path.join('instance', 'odds_history.db')
    
    if not os.path.exists(db_path):
        print("Database doesn't exist yet. No migration needed.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get current table structure
    cursor.execute("PRAGMA table_info(odds_record)")
    columns = [row[1] for row in cursor.fetchall()]
    
    print(f"Current columns: {columns}")
    
    # Add missing columns
    migrations = []
    
    if 'home_team' not in columns:
        migrations.append("ALTER TABLE odds_record ADD COLUMN home_team VARCHAR(100)")
        print("✓ Will add home_team column")
    
    if 'away_team' not in columns:
        migrations.append("ALTER TABLE odds_record ADD COLUMN away_team VARCHAR(100)")
        print("✓ Will add away_team column")
    
    if 'actual_result' not in columns:
        migrations.append("ALTER TABLE odds_record ADD COLUMN actual_result VARCHAR(1)")
        print("✓ Will add actual_result column")
    
    if 'is_completed' not in columns:
        migrations.append("ALTER TABLE odds_record ADD COLUMN is_completed BOOLEAN DEFAULT 0")
        print("✓ Will add is_completed column")
    
    # Execute migrations
    if migrations:
        print(f"\nExecuting {len(migrations)} migrations...")
        for migration in migrations:
            try:
                cursor.execute(migration)
                print(f"✓ Executed: {migration}")
            except sqlite3.OperationalError as e:
                print(f"✗ Error: {e}")
        
        conn.commit()
        print("\n✓ Database migration completed successfully!")
    else:
        print("\n✓ Database is already up to date!")
    
    # Show updated structure
    cursor.execute("PRAGMA table_info(odds_record)")
    columns_after = cursor.fetchall()
    print("\nUpdated table structure:")
    for col in columns_after:
        print(f"  - {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == '__main__':
    migrate_database()
