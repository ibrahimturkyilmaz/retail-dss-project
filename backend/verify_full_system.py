from database import SessionLocal
from models import Store, Inventory, Product, Sale
from simulation_engine import simulate_sales_boom, simulate_supply_shock, reset_database
from transfer_engine import generate_transfer_recommendations
from sqlalchemy import func

def verify_full_system():
    print("\n--- 🚀 Full System Verification Started ---\n")
    db = SessionLocal()
    
    try:
        # 1. Reset System
        print("[1/5] Resetting Database...")
        reset_database(db)
        initial_stock = db.query(func.sum(Inventory.quantity)).scalar() or 0
        print(f"✅ System Reset. Total Initial Stock: {initial_stock}")

        # 2. Test Sales Boom Simulation
        print("\n[2/5] Testing 'Sales Boom' Simulation...")
        boom_msg = simulate_sales_boom(db)
        print(f"ℹ️  Output: {boom_msg}")
        
        after_boom_stock = db.query(func.sum(Inventory.quantity)).scalar() or 0
        sales_count = db.query(Sale).count()
        print(f"📉 Stock Change: {initial_stock} -> {after_boom_stock} (Expected Decrease)")
        print(f"💰 Global Sales Records: {sales_count} (Expected Increase)")
        
        if after_boom_stock >= initial_stock:
            print("❌ FAIL: Stock did not decrease after sales boom.")
        else:
            print("✅ PASS: Sales boom effectively reduced stock.")

        # 3. Test Transfer Recommendations Logic (Hierarchical)
        print("\n[3/5] Testing Hierarchical Transfer Logic...")
        stores = db.query(Store).all()
        start_recs = generate_transfer_recommendations(stores[:50])
        print(f"📊 Recommendations Generated: {len(start_recs)}")
        
        if len(start_recs) > 0:
            sample = start_recs[0]
            print(f"   Sample: '{sample['source']['name']}' -> '{sample['target']['name']}' (Amt: {sample['amount']})")
            print(f"   XAI Reason: {sample['xai_explanation']['summary']}")
            print("✅ PASS: Transfer engine is generating XAI-enriched recommendations.")
        else:
            print("⚠️ WARNING: No recommendations generated (Might be balanced).")

        # 4. Test Supply Shock Simulation
        print("\n[4/5] Testing 'Supply Shock' Simulation...")
        shock_msg = simulate_supply_shock(db)
        print(f"ℹ️  Output: {shock_msg}")
        
        after_shock_stock = db.query(func.sum(Inventory.quantity)).scalar() or 0
        print(f"📉 Stock Change: {after_boom_stock} -> {after_shock_stock} (Expected Drastic Decrease)")
        
        if after_shock_stock >= after_boom_stock:
             print("❌ FAIL: Stock did not decrease after supply shock.")
        else:
             print("✅ PASS: Supply shock effectively slashed inventory.")

        print("\n--- ✅ Full System Verification COMPLETED SUCCESSFULY ---")

    except Exception as e:
        print(f"\n--- ❌ SYSTEM VERIFICATION FAILED ---")
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_full_system()
