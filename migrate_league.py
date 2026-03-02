"""
Database Migration: Add league column to OddsRecord table
Run this script to update your existing database with the new league field
"""

import sqlite3
import os

def migrate_database():
    db_path = 'instance/odds_history.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("✓ Database doesn't exist yet - will be created automatically")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if league column already exists
        cursor.execute("PRAGMA table_info(odds_record)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'league' in columns:
            print("✓ League column already exists - no migration needed")
        else:
            print("Adding league column to odds_record table...")
            cursor.execute("ALTER TABLE odds_record ADD COLUMN league VARCHAR(100)")
            conn.commit()
            print("✓ League column added successfully!")
        
        conn.close()
        print("\n✓ Migration complete!")
        
    except Exception as e:
        print(f"✗ Migration error: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 50)
    print("DATABASE MIGRATION - Adding League Field")
    print("=" * 50)
    migrate_database()
