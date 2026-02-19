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

def reset_user(email):
    db = SyncSessionLocal()
    try:
        print(f"Searching for user with email: {email}")
        
        # 1. Delete from Customers
        customer = db.query(Customer).filter(Customer.email == email).first()
        if customer:
            print(f"Found Customer (ID: {customer.id}, Name: {customer.name}). Deleting...")
            db.delete(customer)
        else:
            print("Customer record not found.")

        # 2. Delete from Users (if exists - usually for web dashboard)
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"Found User (ID: {user.id}, Username: {user.username}). Deleting...")
            db.delete(user)
        else:
            print("User record not found.")
            
        db.commit()
        print("✅ Reset Complete! You can now login again to trigger the Welcome Email.")
        
    except Exception as e:
        print(f"❌ Error during reset: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = input("Enter email to reset: ")
    
    reset_user(email)
