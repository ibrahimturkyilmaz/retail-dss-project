from database import SessionLocal
from models import Sale
from sqlalchemy import func

def verify_data():
    db = SessionLocal()
    try:
        total = db.query(Sale).count()
        weather_nulls = db.query(Sale).filter(Sale.weather == None).count()
        holiday_nulls = db.query(Sale).filter(Sale.holiday == None).count()
        promo_not_null = db.query(Sale).filter(Sale.promotion != None).count()
        
        print(f"--- Data Refinement Verification ---")
        print(f"Total Sales: {total}")
        print(f"Weather Nulls: {weather_nulls} (Should be 0)")
        print(f"Holiday Nulls: {holiday_nulls} (Should be ~0)")
        print(f"Promotions Active: {promo_not_null} (Should be ~15% of total)")
        
        print("\n--- Sample Records ---")
        samples = db.query(Sale).limit(5).all()
        for s in samples:
            print(f"ID: {s.id} | Date: {s.date} | Weather: {s.weather} | Holiday: {s.holiday} | Promo: {s.promotion}")
            
    finally:
        db.close()

if __name__ == "__main__":
    verify_data()
