import requests
import json
import random

BASE_URL = "http://localhost:8000/api"

def test_loyalty_flow():
    print("🚀 Starting Loyalty Flow Test...")
    
    # 1. Create Customer
    phone = f"555{random.randint(1000000, 9999999)}"
    customer_payload = {
        "name": "Loyalty Tester",
        "phone": phone,
        "email": f"test_{phone}@example.com",
        "city": "Istanbul"
    }
    
    print(f"1. Creating Customer ({phone})...")
    res = requests.post(f"{BASE_URL}/customers/", json=customer_payload)
    if res.status_code != 200:
        print(f"❌ Customer Create Failed: {res.text}")
        return
    
    customer = res.json()
    cust_id = customer['id']
    print(f"✅ Customer Created: ID={cust_id}, Points={customer['points_balance']}")

    # 2. Make Sale 1 (Earn Points)
    print("\n2. Making Sale (1000 TL) to Earn Points...")
    sale_payload = {
        "pos_device_id": "TEST-POS-01",
        "receipt_no": f"R-{random.randint(100000, 999999)}",
        "transaction_type": "SALE",
        "total_amount": 1000.0,
        "currency": "TRY",
        "items": [
            {"product_sku": "8690000000001", "quantity": 1, "unit_price": 1000.0, "vat_rate": 18.0}
        ],
        "payments": [{"payment_method": "CREDIT_CARD", "amount": 1000.0}],
        "created_at": "2024-01-01T10:00:00"
    }
    
    # We pass customer_id via query param as implemented in frontend
    res = requests.post(f"{BASE_URL}/pos/sales?customer_id={cust_id}", json=sale_payload)
    if res.status_code != 200:
        print(f"❌ Sale 1 Failed: {res.text}")
        return
    
    data = res.json()
    earned = data.get('points_earned', 0)
    print(f"✅ Sale 1 Complete. Earned: {earned} Points")
    
    # 3. Check Balance
    print("\n3. Checking Customer Balance...")
    # Search by phone to get fresh data
    res = requests.get(f"{BASE_URL}/customers/search?q={phone}")
    customers = res.json()
    fresh_cust = customers[0]
    balance = fresh_cust['points_balance']
    shopping_count = fresh_cust['total_shopping_count']
    print(f"✅ Balance: {balance} (Expected ~1000), Shopping Count: {shopping_count}")

    if balance < 1000:
        print("❌ Points calculation seems wrong!")

    # 4. Make Sale 2 (Use Points)
    # Suppose we buy something for 500 TL and use 500 Points.
    print(f"\n4. Making Sale 2 (500 TL) using 500 Points...")
    
    points_to_use = 500.0
    sale2_payload = {
        "pos_device_id": "TEST-POS-01",
        "receipt_no": f"R-{random.randint(100000, 999999)}",
        "transaction_type": "SALE",
        "total_amount": 500.0,
        "currency": "TRY",
        "items": [
            {"product_sku": "8690000000002", "quantity": 1, "unit_price": 500.0, "vat_rate": 18.0}
        ],
        "payments": [
            {"payment_method": "POINTS", "amount": points_to_use},
            # {"payment_method": "CREDIT_CARD", "amount": 0.0} # Optional if full covered
        ],
        "created_at": "2024-01-01T12:00:00"
    }
    
    res = requests.post(f"{BASE_URL}/pos/sales?customer_id={cust_id}", json=sale2_payload)
    if res.status_code != 200:
        print(f"❌ Sale 2 Failed: {res.text}")
        return
        
    data2 = res.json()
    earned2 = data2.get('points_earned', 0)
    print(f"✅ Sale 2 Complete. Earned: {earned2} Points (from Total Amount)")

    # 5. Final Check
    print("\n5. Checking Final Balance...")
    res = requests.get(f"{BASE_URL}/customers/search?q={phone}")
    final_cust = res.json()[0]
    final_balance = final_cust['points_balance']
    print(f"✅ Final Balance: {final_balance} (Expected: {balance} - {points_to_use} + {earned2})")
    
    expected = balance - points_to_use + earned2
    if abs(final_balance - expected) < 0.1:
        print("🎉 SUCCESS! Logic Verified.")
    else:
        print(f"❌ FAILURE! Expected {expected} but got {final_balance}")

if __name__ == "__main__":
    test_loyalty_flow()
