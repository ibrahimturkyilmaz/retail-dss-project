from database import SyncSessionLocal
from models import Store
from sqlalchemy import select

def get_store_coords():
    db = SyncSessionLocal()
    try:
        store = db.query(Store).first()
        if store:
            print(f"Store: {store.name}")
            print(f"Lat: {store.lat}")
            print(f"Lon: {store.lon}")
            print(f"ID: {store.id}")
        else:
            print("No stores found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    get_store_coords()
