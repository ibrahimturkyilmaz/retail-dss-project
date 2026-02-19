from database import get_sync_db
from models import Product
import random

def assign_numeric_barcodes():
    db = next(get_sync_db())
    products = db.query(Product).all()
    
    print(f"Assigning numeric barcodes to {len(products)} products...")
    
    # Start EAN-13 prefix for TR (869) + random or sequential
    # Let's use sequential for predictability in simulation: 8690000000001
    
    base_code = 8690000000000
    
    for i, p in enumerate(products):
        # Generate a 13-digit number
        new_barcode = str(base_code + i + 1)
        p.sku = new_barcode
        print(f"Product: {p.name} -> New Barcode: {new_barcode}")
        
    db.commit()
    print("✅ Numeric barcodes assigned.")

if __name__ == "__main__":
    assign_numeric_barcodes()
