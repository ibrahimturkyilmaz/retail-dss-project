from database import engine
from sqlalchemy import text

def add_sku_column():
    print("Migrating: Adding SKU to products table...")
    try:
        with engine.begin() as conn:
            # SQLite supports ADD COLUMN
            conn.execute(text("ALTER TABLE products ADD COLUMN sku VARCHAR"))
            print("✅ Migration successful: Added sku to products table.")
            
            # Indexes/Unique constraints usually require more complex migration in SQLite
            # We will skip adding constraint at DB level for now to avoid data loss risk
            # but models.py has it defined for future.
    except Exception as e:
        print(f"⚠️ Migration failed (maybe column exists): {e}")

if __name__ == "__main__":
    add_sku_column()
