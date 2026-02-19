import asyncio
from httpx import AsyncClient, ASGITransport
from main import app
import datetime

async def test_phase6():
    print("Testing Phase 6 Endpoints...")
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Test Random Product
        print("\n1. Testing Random Product...")
        res = await client.get("/api/pos/products/random")
        if res.status_code == 200:
            product = res.json()
            print(f"✅ Random Product: {product['name']} ({product['sku']}) - {product['price']} TL")
        else:
            print(f"❌ Random Product Failed: {res.text}")
            return

        # 2. Test Sales (Direct)
        print("\n2. Testing Direct Sale...")
        payload = {
            "pos_device_id": "POS-TEST-PHASE6",
            "receipt_no": f"R-TEST-{datetime.datetime.now().timestamp()}",
            "transaction_type": "SALE",
            "total_amount": product['price'],
            "currency": "TRY",
            "items": [
                {"product_sku": product['sku'], "quantity": 1, "unit_price": product['price']}
            ],
            "payments": [
                {"payment_method": "CASH", "amount": product['price']}
            ]
        }
        
        # Test with Email
        email = "test_phase6@example.com"
        res = await client.post(f"/api/pos/sales?email={email}", json=payload)
        
        if res.status_code == 200:
            data = res.json()
            print(f"✅ Sale Successful. Receipt ID: {data['receipt_no']}")
        else:
            print(f"❌ Sale Failed: {res.text}")

if __name__ == "__main__":
    asyncio.run(test_phase6())
