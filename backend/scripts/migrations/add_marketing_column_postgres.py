import sys
import os
import asyncio
from sqlalchemy import text

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database import async_engine

async def add_columns():
    async with async_engine.begin() as conn:
        print("Connecting to Supabase (PostgreSQL)...")
        
        columns_to_add = [
            ("interested_in_marketing", "BOOLEAN DEFAULT FALSE"),
            ("engagement_score", "FLOAT DEFAULT 1.0")
        ]
        
        for col_name, col_type in columns_to_add:
            try:
                print(f"Adding column '{col_name}'...")
                await conn.execute(text(f"ALTER TABLE customers ADD COLUMN {col_name} {col_type}"))
                print(f"✅ Column '{col_name}' added successfully.")
            except Exception as e:
                # PostgreSQL error for duplicate column usually contains "algorithm" or specific code, 
                # but generic exception catching is fine for this script
                if "already exists" in str(e):
                    print(f"⚠️ Column '{col_name}' already exists. Skipping.")
                else:
                    print(f"❌ Error adding column '{col_name}': {e}")
                    
    print("Migration complete.")

if __name__ == "__main__":
    asyncio.run(add_columns())
