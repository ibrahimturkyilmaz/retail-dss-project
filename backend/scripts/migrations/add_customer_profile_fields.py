"""
DB Migration: Customer model'e surname, photo_url, email_verified ekleme.
Çalıştır: python add_customer_profile_fields.py
"""
import asyncio
from sqlalchemy import text
from database import async_engine

async def migrate():
    async with async_engine.begin() as conn:
        # Check and add surname column
        try:
            await conn.execute(text("ALTER TABLE customers ADD COLUMN surname VARCHAR"))
            print("✅ surname column added")
        except Exception as e:
            print(f"⚠️ surname: {e}")
        
        # Check and add photo_url column
        try:
            await conn.execute(text("ALTER TABLE customers ADD COLUMN photo_url VARCHAR"))
            print("✅ photo_url column added")
        except Exception as e:
            print(f"⚠️ photo_url: {e}")
        
        # Check and add email_verified column
        try:
            await conn.execute(text("ALTER TABLE customers ADD COLUMN email_verified BOOLEAN DEFAULT FALSE"))
            print("✅ email_verified column added")
        except Exception as e:
            print(f"⚠️ email_verified: {e}")
    
    print("\n🎉 Migration complete!")

if __name__ == "__main__":
    asyncio.run(migrate())
