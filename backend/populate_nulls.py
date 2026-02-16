import random
from datetime import date
import time
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Sale, Base
from sqlalchemy import text, update

def get_season_weather(d: date):
    month = d.month
    if month in [12, 1, 2]:
        return random.choice(["Snowy", "Rainy", "Cloudy", "Cold"])
    elif month in [3, 4, 5]:
        return random.choice(["Rainy", "Cloudy", "Sunny", "Mild"])
    elif month in [6, 7, 8]:
        return random.choice(["Sunny", "Clear", "Hot", "Humid"])
    else: # 9, 10, 11
        return random.choice(["Rainy", "Windy", "Cloudy", "Cool"])

def get_holiday(d: date):
    # Simple TR Holidays logic
    day, month = d.day, d.month
    if month == 1 and day == 1: return "New Year"
    if month == 4 and day == 23: return "National Sovereignty Day"
    if month == 5 and day == 19: return "Youth and Sports Day"
    if month == 7 and day == 15: return "Democracy Day"
    if month == 8 and day == 30: return "Victory Day"
    if month == 10 and day == 29: return "Republic Day"
    if random.random() < 0.02: return "Local Event"
    return None

def get_promotion():
    if random.random() < 0.15: 
        return random.choice(["10% Off", "Buy 1 Get 1", "Weekend Sale", "Clearance"])
    return None

def populate_missing_fields():
    print("Connecting to database...", flush=True)
    db = SessionLocal()
    try:
        # Check total to do
        total_remaining = db.query(Sale).filter(Sale.weather == None).count()
        print(f"Total null records to update: {total_remaining}", flush=True)
        
        chunk_size = 1000
        total_updated = 0
        
        while True:
            t0 = time.time()
            # Fetch PK and Date
            print(f"Fetching next {chunk_size} records...", flush=True)
            sales = db.query(Sale).filter(Sale.weather == None).limit(chunk_size).all()
            
            if not sales:
                break
            
            mappings = []
            for sale in sales:
                mappings.append({
                    "id": sale.id,
                    "weather": get_season_weather(sale.date),
                    "holiday": get_holiday(sale.date),
                    "promotion": get_promotion()
                })
            
            # Bulk Update
            t1 = time.time()
            print(f"Updating {len(mappings)} records in DB...", flush=True)
            
            # Use core update for speed? No, bulk_update_mappings is fine
            db.bulk_update_mappings(Sale, mappings)
            db.commit()
            
            total_updated += len(mappings)
            t2 = time.time()
            print(f"Updated chunk in {t2-t0:.2f}s. Total: {total_updated}", flush=True)
            
        print(f"✅ DONE! Successfully updated {total_updated} records.", flush=True)
        
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_missing_fields()
