from database import async_engine
import asyncio
from sqlalchemy import text

async def update_db():
    async with async_engine.begin() as conn:
        # 1. Update Customers Table
        print("Updating customers table...")
        try:
            await conn.execute(text("ALTER TABLE customers ADD COLUMN phone VARCHAR"))
            await conn.execute(text("ALTER TABLE customers ADD COLUMN email VARCHAR"))
            await conn.execute(text("ALTER TABLE customers ADD COLUMN points_balance FLOAT DEFAULT 0"))
            await conn.execute(text("ALTER TABLE customers ADD COLUMN total_shopping_count INTEGER DEFAULT 0"))
            print("✅ Customers table updated.")
        except Exception as e:
            print(f"⚠️ Customers table update skipped (Maybe already exists): {e}")

        # 2. Update PosSales Table
        print("Updating pos_sales table...")
        try:
            await conn.execute(text("ALTER TABLE pos_sales ADD COLUMN loyalty_points_earned FLOAT DEFAULT 0"))
            await conn.execute(text("ALTER TABLE pos_sales ADD COLUMN loyalty_points_used FLOAT DEFAULT 0"))
            print("✅ PosSales table updated.")
        except Exception as e:
            print(f"⚠️ PosSales table update skipped: {e}")

if __name__ == "__main__":
    asyncio.run(update_db())
