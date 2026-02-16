from database import SessionLocal
from models import Sale
import random

def debug_update():
    print("Connecting...")
    db = SessionLocal()
    try:
        # Get one sale
        sale = db.query(Sale).first()
        if not sale:
            print("No sales found!")
            return

        print(f"Found Sale ID: {sale.id}, Weather: {sale.weather}")
        
        # Update
        print("Updating weather to 'DEBUG_SUNNY'...")
        sale.weather = "DEBUG_SUNNY"
        db.commit()
        db.refresh(sale)
        
        print(f"Updated Sale ID: {sale.id}, Weather: {sale.weather}")
        print("✅ Single update successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    debug_update()
