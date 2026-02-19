from database import get_sync_db
from models import Store, Inventory, Product

def create_field_store():
    db = next(get_sync_db())
    try:
        # Check if store exists
        field_store = db.query(Store).filter(Store.id == 9999).first()
        if not field_store:
            print("Creating Field Operations Store (ID: 9999)...")
            field_store = Store(
                id=9999,
                name="Saha Operasyon Deposu",
                store_type="HUB",
                lat=41.0082,  # Istanbulish
                lon=28.9784,
                # stock ve safety_stock Inventory tablosunda tutulur, Store modelinde değil.
            )
            db.add(field_store)
            db.commit()
            print("✅ Field Store Created.")
        else:
            print("ℹ️ Field Store already exists.")

        # Populate Inventory for Field Store
        products = db.query(Product).all()
        print(f"Populating inventory for {len(products)} products in Field Store...")
        
        for p in products:
            inv = db.query(Inventory).filter(
                Inventory.store_id == 9999, 
                Inventory.product_id == p.id
            ).first()
            
            if not inv:
                inv = Inventory(
                    store_id=9999,
                    product_id=p.id,
                    quantity=500, # Initial stock for field ops
                    safety_stock=50
                )
                db.add(inv)
                
        db.commit()
        print("✅ Field Store Inventory Populated.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_field_store()
