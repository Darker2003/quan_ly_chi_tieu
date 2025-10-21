"""
Migration script to add is_admin column to users table
"""

import sqlite3


def migrate():
    """Add is_admin column to users table"""
    conn = sqlite3.connect('moneyflow.db')
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_admin' in columns:
            print("✅ Column 'is_admin' already exists!")
            return
        
        # Add the column
        print("Adding 'is_admin' column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0")
        conn.commit()
        print("✅ Successfully added 'is_admin' column!")
        
        # Verify
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"\n📋 Current columns in users table:")
        for col in columns:
            print(f"  • {col}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()

