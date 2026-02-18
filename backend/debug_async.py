import asyncio
from database import get_db
from sqlalchemy import text
from models import Product, Store

async def test_connection():
    try:
        print("Testing Async Connection...")
        async for session in get_db():
            print("Session acquired.")
            result = await session.execute(text("SELECT 1"))
            print(f"Query Result: {result.scalar()}")
            
            # Test Store query
            print("Querying Stores...")
            from sqlalchemy.future import select
            from sqlalchemy.orm import selectinload
            stmt = select(Store).options(selectinload(Store.features), selectinload(Store.inventory))
            res = await session.execute(stmt)
            stores = res.scalars().all()
            print(f"Stores found: {len(stores)}")
            for s in stores:
                 print(f"Store: {s.name}, Type: {s.store_type}, Inv: {len(s.inventory)}")
                 
            # Test Sales query
            print("Querying Sales...")
            from models import Sale
            stmt2 = select(Sale).options(selectinload(Sale.store)).limit(5)
            res2 = await session.execute(stmt2)
            sales = res2.scalars().all()
            print(f"Sales found: {len(sales)}")
            
            break
        print("✅ Async Connection Successful")
    except Exception as e:
        print(f"❌ Async Connection Failed: {e}")
        import traceback
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
