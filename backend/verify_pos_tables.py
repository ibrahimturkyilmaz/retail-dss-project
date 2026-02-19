from database import engine, Base
from models import PosSale, PosSaleItem, PosPayment, PosZReport
from sqlalchemy import inspect
import asyncio

def verify_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    required_tables = ["pos_sales", "pos_sale_items", "pos_payments", "pos_z_reports"]
    missing = [t for t in required_tables if t not in tables]
    
    if missing:
        print(f"❌ Missing tables: {missing}")
        # Try creating them
        print("Attempting to create tables...")
        Base.metadata.create_all(bind=engine)
        
        # Check again
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        missing = [t for t in required_tables if t not in tables]
        if missing:
             print(f"❌ Still missing after create_all: {missing}")
        else:
             print("✅ Tables created successfully!")
    else:
        print("✅ All POS tables exist.")

if __name__ == "__main__":
    verify_tables()
