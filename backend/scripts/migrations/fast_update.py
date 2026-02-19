from database import SessionLocal
from sqlalchemy import text

def fast_update():
    print("Connecting to DB...", flush=True)
    db = SessionLocal()
    try:
        print("Starting SQL updates...", flush=True)
        
        # 1. Weather (Season based)
        print("Updating Weather...", flush=True)
        db.execute(text("UPDATE sales SET weather = 'Snowy' WHERE EXTRACT(MONTH FROM date) IN (12, 1, 2) AND weather IS NULL"))
        db.execute(text("UPDATE sales SET weather = 'Rainy' WHERE EXTRACT(MONTH FROM date) IN (3, 4, 5) AND weather IS NULL")) # Spring
        db.execute(text("UPDATE sales SET weather = 'Sunny' WHERE EXTRACT(MONTH FROM date) IN (6, 7, 8) AND weather IS NULL")) # Summer
        db.execute(text("UPDATE sales SET weather = 'Cloudy' WHERE EXTRACT(MONTH FROM date) IN (9, 10, 11) AND weather IS NULL")) # Autumn
        
        # 2. Holiday (Specific Dates)
        print("Updating Holidays...", flush=True)
        holidays = [
            (1, 1, 'New Year'),
            (4, 23, 'National Sovereignty Day'),
            (5, 19, 'Youth and Sports Day'),
            (7, 15, 'Democracy Day'),
            (8, 30, 'Victory Day'),
            (10, 29, 'Republic Day')
        ]
        for m, d, name in holidays:
            # Use params strictly speaking, but for this fixed list string formatting is safe enough and clearer for debug
            stmt = text(f"UPDATE sales SET holiday = :name WHERE EXTRACT(MONTH FROM date) = :m AND EXTRACT(DAY FROM date) = :d")
            db.execute(stmt, {"name": name, "m": m, "d": d})
            
        # 3. Promotion (Random 15%)
        print("Updating Promotions...", flush=True)
        # PostgreSQL random() returns 0.0 to 1.0
        db.execute(text("UPDATE sales SET promotion = '10% Off' WHERE promotion IS NULL AND random() < 0.15"))
        
        db.commit()
        print("✅ DONE! All updates committed.", flush=True)
        
    except Exception as e:
        print(f"❌ Error: {e}", flush=True)
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fast_update()
