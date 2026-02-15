from database import SessionLocal
from export_engine import export_training_data

def test_export_direct():
    print("Testing export_training_data() directly...")
    
    db = SessionLocal()
    try:
        # Mağaza 1, Ürün 1 için test
        csv_content = export_training_data(db, store_id=1, product_id=1)
        
        if csv_content:
            print("✅ Data retrieved successfully")
            lines = csv_content.split('\n')
            print(f"✅ Header: {lines[0].strip()}")
            print(f"✅ First Row: {lines[1].strip()}")
            print(f"✅ Total Rows: {len(lines)}")
            
            if "ds,y" in lines[0]:
                print("✅ Format check PASSED (Prophet compatible)")
            else:
                print("❌ Format check FAILED")
        else:
            print("❌ No data returned (Empty CSV)")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_export_direct()

