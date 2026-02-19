import asyncio
from httpx import AsyncClient, ASGITransport
from main import app
import datetime

async def test_sync():
    print("Testing POS Sync Endpoint (AsyncHTTPX)...")
    
    # Create transport for ASGI app
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "pos_device_id": "POS-MODERN-01",
            "receipt_no": "R-2002",
            "transaction_type": "SALE",
            "total_amount": 250.0,
            "items": [
                {"product_sku": "SKU-ASYNC", "quantity": 2, "unit_price": 125.0}
            ],
            "payments": [
                {"payment_method": "CREDIT_CARD", "amount": 250.0}
            ],
            "created_at": datetime.datetime.now().isoformat()
        }

        try:
            # 1. First Request
            print("Sending First Request...")
            response = await client.post("/api/pos/sync", json=payload)
            print(f"Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ Failed: {response.text}")
                return

            data = response.json()
            print(f"✅ Created Sale ID: {data['id']}")
            first_id = data['id']

            # 2. Idempotency Request
            print("Sending Duplicate Request...")
            response2 = await client.post("/api/pos/sync", json=payload)
            print(f"Status: {response2.status_code}")
            data2 = response2.json()
            
            if data2['id'] == first_id:
                print("✅ Idempotency Check Passed")
            else:
                print(f"❌ Idempotency Failed: {data2['id']}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_sync())
