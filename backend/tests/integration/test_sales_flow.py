import pytest
import time
from httpx import AsyncClient, ASGITransport
import os
import sys

# Ensure backend path is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from main import app
from core.config import settings

# Override settings for test environment if needed
# (Assuming .env is loaded correctly by config.py or enviroment variables)

@pytest.mark.asyncio
async def test_full_sales_flow_integration():
    """
    Simulates a full sales flow:
    1. Create/Check Customer
    2. Add Product to Cart
    3. Complete Sale (with Email Trigger)
    4. Verify Response
    """
    
    # Setup Test Client
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as client:
        
        # --- 1. Customer Setup ---
        target_email = "ibrahimtrkylmz632@gmail.com"
        customer_name = "Integration Test User"
        
        cust_payload = {
            "name": customer_name,
            "phone": "5559998877", # Unique test phone
            "email": target_email,
            "city": "TestCity"
        }

        # Try to create
        res = await client.post("/api/customers", json=cust_payload)
        
        cust_id = None
        if res.status_code == 200:
            cust_id = res.json()['id']
            print(f"✅ Created Test Customer: {cust_id}")
        elif res.status_code == 400:
            # Check if exists via search
            res_search = await client.get(f"/api/customers/search?q={cust_payload['phone']}")
            assert res_search.status_code == 200
            found = res_search.json()
            assert len(found) > 0
            cust_id = found[0]['id']
            print(f"ℹ️ Used Existing Customer: {cust_id}")
        else:
            pytest.fail(f"Customer creation failed: {res.text}")

        # --- 2. Product Selection ---
        # Get random product
        res_prod = await client.get("/api/pos/products/random")
        if res_prod.status_code == 200:
            prod = res_prod.json()
            sku = prod['sku']
            price = prod['price']
            print(f"📦 Selected Product: {prod['name']} ({sku})")
        else:
             # Fallback logic or fail
             # For integration test, we expect products to exist in the real DB.
             # If not, maybe we should skip or insert one.
             pytest.fail("No products found in DB for test.")

        # --- 3. Execute Sale ---
        receipt_no = f"REC-INT-{int(time.time())}"
        sale_payload = {
            "pos_device_id": "TEST-CI-CD",
            "receipt_no": receipt_no,
            "transaction_type": "SALE",
            "total_amount": price,
            "currency": "TRY",
            "created_at": None,
            "items": [
                {"product_sku": sku, "quantity": 1, "unit_price": price, "vat_rate": 18}
            ],
            "payments": [
                {"payment_method": "CREDIT_CARD", "amount": price}
            ]
        }
        
        print(f"💳 Processing Sale {receipt_no}...")
        res_sale = await client.post(
            f"/api/pos/sales?customer_id={cust_id}&email={target_email}", 
            json=sale_payload
        )
        
        # Assertions
        assert res_sale.status_code == 200, f"Sale failed: {res_sale.text}"
        data = res_sale.json()
        assert data['receipt_no'] == receipt_no
        assert data['total_amount'] == price
        assert 'points_earned' in data
        
        print("✅ Sale Successful & Verified!")
