from database import SessionLocal
from models import Store, Inventory, Product
from risk_engine import analyze_store_risk, get_risk_report
from transfer_engine import generate_transfer_recommendations

def verify_backend():
    print("--- Backend Verification Start ---")
    db = SessionLocal()
    
    try:
        # 1. Check Data Existence
        stores = db.query(Store).all()
        products = db.query(Product).all()
        inventory_count = db.query(Inventory).count()
        
        print(f"Stores: {len(stores)}")
        print(f"Products: {len(products)}")
        print(f"Inventory Records: {inventory_count}")
        
        if len(stores) == 0 or len(products) == 0 or inventory_count == 0:
            print("FAIL: Database seems empty.")
            return

        # 2. Check Relationships (Store -> Inventory)
        sample_store = stores[0]
        print(f"Checking Store: {sample_store.name}")
        print(f"Inventory Items: {len(sample_store.inventory)}")
        
        if len(sample_store.inventory) == 0:
            print("FAIL: Store has no inventory linked.")
            return

        # 3. Check Risk Engine
        print("\nTesting Risk Engine...")
        risk_status = analyze_store_risk(sample_store)
        print(f"Store Risk Status: {risk_status}")
        
        report = get_risk_report(stores)
        print(f"Risk Report Generated for {len(report)} stores.")

        # 4. Check Transfer Engine
        print("\nTesting Transfer Engine (Robin Hood)...")
        recommendations = generate_transfer_recommendations(stores)
        print(f"Recommendations Generated: {len(recommendations)}")
        if len(recommendations) > 0:
            print(f"Sample Rec: {recommendations[0]['reasons']}")
        
        print("\n--- Backend Verification PASS ---")
        
    except Exception as e:
        print(f"\n--- Backend Verification FAIL ---")
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_backend()
