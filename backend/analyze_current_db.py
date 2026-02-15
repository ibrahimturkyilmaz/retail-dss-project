from sqlalchemy import text, inspect
from database import SessionLocal, engine
from models import Store, Product, Sale

def analyze_db():
    db = SessionLocal()
    inspector = inspect(engine)
    
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("--- Database Analysis Report ---\n")
        
        # 1. Table Existence Check
        tables = inspector.get_table_names()
        f.write(f"Existing Tables: {tables}\n")
        
        # 2. Row Counts
        store_count = db.query(Store).count()
        product_count = db.query(Product).count()
        sale_count = db.query(Sale).count()
        
        f.write(f"\n--- Row Counts ---\n")
        f.write(f"Stores: {store_count}\n")
        f.write(f"Products: {product_count}\n")
        f.write(f"Sales Records: {sale_count}\n")
        
        # 3. Sales Data Analysis (Time Range)
        if sale_count > 0:
            min_date = db.query(text("min(date)")).select_from(Sale).scalar()
            max_date = db.query(text("max(date)")).select_from(Sale).scalar()
            f.write(f"\n--- Sales Data Range ---\n")
            f.write(f"Start Date: {min_date}\n")
            f.write(f"End Date: {max_date}\n")
        else:
            f.write("\n[!] No sales data found!\n")

        # 4. Check for Prophet Requirements
        if sale_count < 100:
             f.write("\n[WARNING] Data volume is extremely low for Prophet.\n")
    
    db.close()
    print("Analysis complete. Check results.txt")

if __name__ == "__main__":
    analyze_db()
