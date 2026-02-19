from starlette.testclient import TestClient
from main import app
import datetime

client = TestClient(app=app)

def test_sync():
    print("Testing POS Sync Endpoint...")
    
    payload = {
        "pos_device_id": "POS-TEST-01",
        "receipt_no": "R-1001",
        "transaction_type": "SALE",
        "total_amount": 150.0,
        "items": [
            {"product_sku": "SKU-999", "quantity": 1, "unit_price": 100.0},
            {"product_sku": "SKU-888", "quantity": 1, "unit_price": 50.0}
        ],
        "payments": [
            {"payment_method": "CASH", "amount": 150.0}
        ],
        "created_at": datetime.datetime.now().isoformat()
    }

    try:
        # 1. First Request
        print("Sending First Request...")
        response = client.post("/api/pos/sync", json=payload)
        print(f"First Request Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Failed: {response.text}")
            return

        data = response.json()
        print(f"✅ Created Sale ID: {data['id']}")
        first_id = data['id']

        # 2. Idempotency Request
        print("Sending Duplicate Request (Idempotency Check)...")
        response2 = client.post("/api/pos/sync", json=payload)
        print(f"Second Request Status: {response2.status_code}")
        data2 = response2.json()
        
        if data2['id'] == first_id:
            print("✅ Idempotency Check Passed: Returned same ID.")
        else:
            print(f"❌ Idempotency Failed: Returned different ID {data2['id']}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    test_sync()
