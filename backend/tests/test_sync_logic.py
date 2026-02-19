import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_engine, AsyncSessionLocal
from models import PosSale, PosSaleItem, Product, Inventory, Store
from sync_engine import process_pending_sales
import datetime

async def test_sync_logic():
    print("Testing Sync Engine Logic...")
    
    async with AsyncSessionLocal() as db:
        try:
            # 1. Setup Test Data
            # Find or Create Test Product
            sku = "SKU-SYNC-TEST"
            prod_query = select(Product).where(Product.sku == sku)
            result = await db.execute(prod_query)
            product = result.scalar_one_or_none()
            
            if not product:
                product = Product(name="Sync Test Product", sku=sku, price=100, cost=50, category="Test")
                db.add(product)
                await db.flush()
                
            # Ensure Inventory Exists for Store 1
            store_id = 1
            inv_query = select(Inventory).where(Inventory.store_id == store_id, Inventory.product_id == product.id)
            result = await db.execute(inv_query)
            inventory = result.scalar_one_or_none()
            
            if not inventory:
                inventory = Inventory(store_id=store_id, product_id=product.id, quantity=100)
                db.add(inventory)
            else:
                inventory.quantity = 100 # Reset for test
                
            await db.commit()
            await db.refresh(inventory)
            
            initial_stock = inventory.quantity
            print(f"Initial Stock: {initial_stock}")
            
            # 2. Create Pending Sale
            sale = PosSale(
                pos_device_id="POS-TEST-SYNC",
                receipt_no=f"R-{datetime.datetime.now().timestamp()}",
                transaction_type="SALE",
                total_amount=100.0,
                status="PENDING"
            )
            db.add(sale)
            await db.flush()
            
            item = PosSaleItem(
                pos_sale_id=sale.id,
                product_sku=sku,
                quantity=5,
                unit_price=20.0
            )
            db.add(item)
            await db.commit()
            
            print(f"Created Pending Sale ID: {sale.id} for 5 items")
            
            # 3. Run Sync Engine
            print("Running process_pending_sales...")
            processed = await process_pending_sales(db)
            print(f"Processed Count: {processed}")
            
            # 4. Verify Results
            # Re-fetch inventory
            await db.refresh(inventory)
            new_stock = inventory.quantity
            print(f"New Stock: {new_stock}")
            
            expected_stock = initial_stock - 5
            if new_stock == expected_stock:
                print("✅ Stock updated correctly.")
            else:
                print(f"❌ Stock update failed. Expected {expected_stock}, got {new_stock}")
                
            # Check Sale Status
            result = await db.execute(select(PosSale).where(PosSale.id == sale.id))
            updated_sale = result.scalar_one()
            if updated_sale.status == "PROCESSED":
                print("✅ Sale status updated to PROCESSED.")
            else:
                 print(f"❌ Sale status failed. Got {updated_sale.status}")
                 
        except Exception as e:
            print(f"❌ Exception: {e}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(test_sync_logic())
