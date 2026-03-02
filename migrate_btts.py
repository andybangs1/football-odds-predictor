"""
Database Migration Script - Add BTTS tracking columns
Adds btts and goals_for columns to odds_record table
"""
import sqlite3
import os

def migrate_btts():
    """Add BTTS tracking columns to odds_record table"""
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
    
    if 'btts' not in columns:
        migrations.append("ALTER TABLE odds_record ADD COLUMN btts VARCHAR(1)")
        print("✓ Will add btts column")
    
    if 'goals_for' not in columns:
        migrations.append("ALTER TABLE odds_record ADD COLUMN goals_for INTEGER")
        print("✓ Will add goals_for column")
    
    # Execute migrations
    if migrations:
        print(f"\nExecuting {len(migrations)} migrations...")
        for migration in migrations:
            try:
                cursor.execute(migration)
                print(f"✓ Executed: {migration}")
            except sqlite3.OperationalError as e:
                if 'already exists' in str(e):
                    print(f"✓ Column already exists: {migration}")
                else:
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
    migrate_btts()
