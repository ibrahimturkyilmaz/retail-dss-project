import sys
import os
import sqlite3

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.config import settings

def add_columns():
    db_path = "retail.db" # Default for SQLite
    if "sqlite" in settings.DATABASE_URL:
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    
    print(f"Connecting to database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    columns_to_add = [
        ("interested_in_marketing", "BOOLEAN DEFAULT 0"),
        ("engagement_score", "FLOAT DEFAULT 1.0")
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            print(f"Adding column '{col_name}'...")
            cursor.execute(f"ALTER TABLE customers ADD COLUMN {col_name} {col_type}")
            print(f"✅ Column '{col_name}' added successfully.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"⚠️ Column '{col_name}' already exists. Skipping.")
            else:
                print(f"❌ Error adding column '{col_name}': {e}")
                
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    add_columns()
