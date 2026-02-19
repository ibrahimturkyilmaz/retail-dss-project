import sys
import os
from dotenv import load_dotenv

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Explicitly load backend .env
backend_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(backend_env_path)

from database import SyncSessionLocal
from models import User, Customer

def list_data():
    db = SyncSessionLocal()
    try:
        customers = db.query(Customer).all()
        users = db.query(User).all()

        print("--- CUSTOMERS (Mobile App) ---")
        if not customers:
            print("(No customers found)")
        for c in customers:
            print(f"ID: {c.id} | Email: {c.email} | Name: {c.name}")

        print("\n--- USERS (Web Dashboard) ---")
        if not users:
            print("(No users found)")
        for u in users:
            print(f"ID: {u.id} | Email: {u.email} | Username: {u.username}")
            
    except Exception as e:
        print(f"Error listing data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_data()
