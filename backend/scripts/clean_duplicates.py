import sys
import os
import asyncio
from sqlalchemy import text
from dotenv import load_dotenv

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Explicitly load backend .env
backend_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(backend_env_path)

from database import async_engine

async def clean_duplicates():
    async with async_engine.begin() as conn:
        print("Cleaning duplicate customers...")
        
        # Identify duplicates (keep the one with the highest ID - latest)
        query = """
        DELETE FROM customers 
        WHERE id NOT IN (
            SELECT MAX(id) 
            FROM customers 
            GROUP BY email
        );
        """
        
        try:
            await conn.execute(text(query))
            print("✅ Duplicates removed. Kept the latest records.")
        except Exception as e:
            print(f"❌ Error cleaning duplicates: {e}")

if __name__ == "__main__":
    asyncio.run(clean_duplicates())
