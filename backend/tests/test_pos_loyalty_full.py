import pytest
import sys
import io

# Force UTF-8 for Windows Console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from unittest.mock import MagicMock

# --- Mock pydantic_settings if missing ---
try:
    import pydantic_settings
except ImportError:
    print("[WARN] pydantic_settings not found. Mocking it...")
    mock_pydantic_settings = MagicMock()
    # Mock BaseSettings
    try:
        from pydantic import BaseModel
        class MockBaseSettings(BaseModel):
            pass
    except ImportError:
        class MockBaseSettings:
            def __init__(self, **kwargs):
                for k,v in kwargs.items():
                    setattr(self, k, v)
    
    mock_pydantic_settings.BaseSettings = MockBaseSettings
    mock_pydantic_settings.SettingsConfigDict = lambda **kwargs: kwargs
    
    sys.modules["pydantic_settings"] = mock_pydantic_settings

# --- Mock slowapi if missing ---
try:
    import slowapi
except ImportError:
    print("[WARN] slowapi not found. Mocking it...")
    mock_slowapi = MagicMock()
    mock_slowapi.Limiter = MagicMock()
    mock_slowapi._rate_limit_exceeded_handler = MagicMock()
    mock_slowapi.util = MagicMock()
    mock_slowapi.util.get_remote_address = MagicMock()
    mock_slowapi.errors = MagicMock()
    mock_slowapi.errors.RateLimitExceeded = Exception
    
    sys.modules["slowapi"] = mock_slowapi
    sys.modules["slowapi.util"] = mock_slowapi.util
    sys.modules["slowapi.errors"] = mock_slowapi.errors

# reportlab mock removed

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Now we can import main
from main import app
from database import get_db, Base
import os
import random

# Use a separate test database
TEST_DATABASE_URL = "sqlite:///./test_retail.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_retail.db"):
        os.remove("./test_retail.db")

def test_loyalty_full_cycle(setup_database):
    print("\n[START] Starting Full Cycle Loyalty Test...")

    # 1. Create Customer
    phone = f"555{random.randint(1000000, 9999999)}"
    customer_payload = {
        "name": "Test User",
        "phone": phone,
        "email": f"test_{phone}@example.com",
        "city": "Test City"
    }
    res = client.post("/api/customers", json=customer_payload)
    assert res.status_code == 200
    customer = res.json()
    cust_id = customer['id']
    print(f"[OK] Customer Created: {cust_id}")

    # 2. Sale 1 (Earn Points)
    # 1000 TL Sale -> Earn Points
    receipt_no_1 = f"R-{random.randint(100000, 999999)}"
    sale1_payload = {
        "pos_device_id": "TEST-POS-01",
        "receipt_no": receipt_no_1,
        "transaction_type": "SALE",
        "total_amount": 1000.0,
        "currency": "TRY",
        "items": [
            {"product_sku": "TEST-SKU-01", "quantity": 1, "unit_price": 1000.0}
        ],
        "payments": [{"payment_method": "CREDIT_CARD", "amount": 1000.0}]
    }
    
    res = client.post(f"/api/pos/sales?customer_id={cust_id}", json=sale1_payload)
    assert res.status_code == 200
    data1 = res.json()
    points_earned_1 = data1['points_earned']
    assert points_earned_1 > 0
    print(f"[OK] Sale 1 Complete. Earned: {points_earned_1}")

    # 3. Verify Balance
    res = client.get(f"/api/customers/{cust_id}")
    cust_after_sale1 = res.json()
    assert cust_after_sale1['points_balance'] == points_earned_1
    
    # 4. Sale 2 (Spend Points)
    # Buy 500 TL item, use 100 Points
    receipt_no_2 = f"R-{random.randint(100000, 999999)}"
    points_to_use = 100.0
    sale2_payload = {
        "pos_device_id": "TEST-POS-01",
        "receipt_no": receipt_no_2,
        "transaction_type": "SALE",
        "total_amount": 500.0,
        "items": [
             {"product_sku": "TEST-SKU-02", "quantity": 1, "unit_price": 500.0}
        ],
        "payments": [
            {"payment_method": "POINTS", "amount": points_to_use},
            {"payment_method": "CASH", "amount": 400.0}
        ]
    }
    
    res = client.post(f"/api/pos/sales?customer_id={cust_id}", json=sale2_payload)
    assert res.status_code == 200
    data2 = res.json()
    points_earned_2 = data2['points_earned']
    print(f"[OK] Sale 2 Complete. Used: {points_to_use}, Earned: {points_earned_2}")

    # 5. Verify Balance After Spend
    res = client.get(f"/api/customers/{cust_id}")
    cust_after_sale2 = res.json()
    expected_balance = points_earned_1 - points_to_use + points_earned_2
    assert abs(cust_after_sale2['points_balance'] - expected_balance) < 0.1
    print(f"[OK] Balance Verified: {cust_after_sale2['points_balance']}")

    # 6. Return Sale 1 (The big earn)
    # Expectation: Points earned (points_earned_1) should be deducted.
    print(f"\n[INFO] Returning Sale 1 (Receipt: {receipt_no_1})...")
    
    res = client.post(f"/api/pos/returns?receipt_no={receipt_no_1}")
    assert res.status_code == 200
    
    # 7. Verify Balance After Return
    res = client.get(f"/api/customers/{cust_id}")
    final_cust = res.json()
    final_balance = final_cust['points_balance']
    
    expected_after_return = expected_balance - points_earned_1
    
    print(f"Checking Return Logic: \nExpected: {expected_after_return} \nActual: {final_balance}")
    
    if abs(final_balance - expected_after_return) < 0.1:
        print("[SUCCESS] Return Logic CORRECT! Points deducted.")
    else:
        print("[FAILURE] Return Logic INCORRECT! Points NOT deducted.")
        # We expect this to fail initially
        raise Exception(f"Points were not deducted after return. Expected {expected_after_return}, got {final_balance}")

if __name__ == "__main__":
    # Manually run if executed as script
    # We need a dummy fixture for direct run or just use the setup logic manually.
    # Simplified manual run:
    print("Running manual test...")
    setup_database_gen = setup_database()
    next(setup_database_gen) # Setup
    try:
        test_loyalty_full_cycle(None)
    except Exception as e:
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(f"Test Failed with Exception: {e}\n")
            import traceback
            traceback.print_exc(file=f)
        print("Logged error to error_log.txt")
    finally:
        try:
            next(setup_database_gen) # Teardown
        except StopIteration:
            pass
