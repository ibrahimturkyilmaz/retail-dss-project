from database import get_sync_db
from models import Product

def populate_skus():
    db = next(get_sync_db())
    products = db.query(Product).all()
    
    print(f"Found {len(products)} products. Assigning SKUs...")
    
    for p in products:
        if not p.sku:
            p.sku = f"SKU-{p.id}"
            print(f"Assigned SKU-{p.id} to {p.name}")
            
    # Add special SKU for testing
    test_sku = "SKU-ASYNC"
    test_prod = db.query(Product).filter(Product.sku == test_sku).first()
    if not test_prod:
        # Create a dummy product for the test SKU if it doesn't exist
        # Or attach it to an existing product if there is one available
        # Let's create a new one to be safe
        new_prod = Product(
            name="Async Test Product",
            category="Test",
            cost=50,
            price=125,
            sku=test_sku
        )
        db.add(new_prod)
        print(f"Created new product for {test_sku}")
        
    db.commit()
    print("✅ SKUs populated.")

if __name__ == "__main__":
    populate_skus()
