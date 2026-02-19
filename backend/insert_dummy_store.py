from database import SyncSessionLocal
from models import Store, StoreType, Customer
import datetime

def insert_data():
    db = SyncSessionLocal()
    try:
        # Check/Insert Store
        store = db.query(Store).filter(Store.name == "Nişantaşı Flagship").first()
        if not store:
            print("Inserting Store...")
            store = Store(
                name="Nişantaşı Flagship",
                store_type=StoreType.STORE,
                lat=41.05,
                lon=28.99,
                last_risk_analysis=datetime.datetime.utcnow()
            )
            db.add(store)
            db.commit()
            db.refresh(store)
            print(f"Store inserted: {store.id}")
        else:
            print(f"Store exists: {store.id}")

        # Check/Insert Customer 32
        customer = db.query(Customer).filter(Customer.id == 32).first()
        if not customer:
            print("Inserting Customer 32...")
            # Ideally we shouldn't force ID, but for demo continuity...
            # SQLAlchemy might not like forcing ID if autoincrement
            # Let's check if we can.
            customer = Customer(
                id=32,
                name="Kemal Yildiz",
                city="Istanbul",
                email="kemal.yildiz@example.com",
                phone="5551234567",
                points_balance=100
            )
            db.add(customer)
            db.commit()
            print("Customer 32 inserted.")
        else:
            print("Customer 32 exists.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    insert_data()
