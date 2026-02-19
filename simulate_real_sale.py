import sys
import os
import io
import time
from unittest.mock import MagicMock

# Force UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

print("🔧 Setting up environment...")

# 1. Mock missing dependencies
# Use robust mocking similar to checks
sys.modules["pydantic_settings"] = MagicMock()
class MockBaseSettings:
    def __init__(self, **kwargs):
        pass
# Assign to module
sys.modules["pydantic_settings"].BaseSettings = MockBaseSettings
sys.modules["pydantic_settings"].SettingsConfigDict = lambda **kwargs: kwargs

# Mock slowapi
mock_slowapi_util = MagicMock()
mock_slowapi_errors = MagicMock()
mock_slowapi = MagicMock()

sys.modules["slowapi"] = mock_slowapi
sys.modules["slowapi.util"] = mock_slowapi_util
sys.modules["slowapi.errors"] = mock_slowapi_errors

# Configure errors
class MockRateLimitExceeded(Exception):
    pass
mock_slowapi_errors.RateLimitExceeded = MockRateLimitExceeded

# Configure util
mock_slowapi_util.get_remote_address = MagicMock()

# Configure main slowapi
mock_slowapi.Limiter = MagicMock()
mock_slowapi._rate_limit_exceeded_handler = MagicMock()
mock_slowapi.util = mock_slowapi_util
mock_slowapi.errors = mock_slowapi_errors

# 2. Load .env manually
env_vars = {}
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
try:
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env_vars[k.strip()] = v.strip()
    print("✅ .env loaded.")
except FileNotFoundError:
    print("❌ .env not found!")
    sys.exit(1)

# 3. Patch Config
try:
    import core.config as config
    # Force defaults if they are missing
    if not hasattr(config.settings, 'TESTING'):
        config.settings.TESTING = False
    
    print(f"🔧 Config settings object: {config.settings}")
    
    # Patch values
    print(f"🔧 Patching DB URL: {env_vars.get('DATABASE_URL')}")
    config.settings.DATABASE_URL = env_vars.get("DATABASE_URL")
    config.settings.MAIL_SERVER = env_vars.get("MAIL_SERVER")
    config.settings.MAIL_PORT = int(env_vars.get("MAIL_PORT", 587))
    config.settings.MAIL_USERNAME = env_vars.get("MAIL_USERNAME")
    config.settings.MAIL_PASSWORD = env_vars.get("MAIL_PASSWORD")
    config.settings.GEMINI_API_KEY = env_vars.get("GEMINI_API_KEY")
    # Cast TESTING to bool
    test_val = env_vars.get("TESTING", "False")
    config.settings.TESTING = str(test_val).lower() in ("true", "1", "t")

except Exception as e:
    print(f"❌ Error patching config: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Import App
print("🚀 Importing FastAPI App... (Async Mode)")
import asyncio
from httpx import AsyncClient, ASGITransport

try:
    from main import app
    print("✅ App initialized.")
except Exception as e:
    print(f"❌ Error importing main/app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

async def simulate_sale_async():
    target_email = "ibrahimtrkylmz632@gmail.com"
    customer_name = "Ibrahim Turkyilmaz"
    
    # Context Manager for App Lifespan (Startup/Shutdown)
    # We use ASGITransport which handles app execution
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as client:
        print(f"\n👤 Checking/Creating Customer: {target_email}...")
        cust_payload = {
            "name": customer_name,
            "phone": "5551234567",
            "email": target_email,
            "city": "Istanbul"
        }
        
        # 1. Create/Check Customer
        res = await client.post("/api/customers", json=cust_payload)
        
        cust_id = None
        if res.status_code == 200:
            customer = res.json()
            print(f"✅ Customer Created: ID {customer['id']}")
            cust_id = customer['id']
        else:
             print(f"ℹ️ Customer create response: {res.status_code}. Checking existing by phone...")
             # Search by Phone
             res_search = await client.get(f"/api/customers/search?q=5551234567")
             if res_search.status_code == 200:
                 found_customers = res_search.json()
                 # Filter by email if possible or just take first matching phone
                 found = next((c for c in found_customers if c.get('email') == target_email), None)
                 
                 if not found and found_customers:
                     # Maybe email didn't match but phone did?
                     print("Found phone match but email different. Picking first match.")
                     found = found_customers[0]
                     
                 if found:
                     cust_id = found['id']
                     print(f"✅ Found Existing Customer: ID {cust_id} ({found['name']})")
                 else:
                     print("❌ Could not create or find customer (Search returned empty).")
                     return
             else:
                 print(f"❌ Could not search customers: {res_search.status_code}")
                 return

        # 2. Prepare Sale
        print("\n🛒 Preparing Sale...")
        res = await client.get("/api/pos/products/random")
        if res.status_code == 200:
            prod = res.json()
            sku = prod['sku']
            price = prod['price']
            print(f"📦 Selected Product: {prod['name']} ({sku}) - {price} TL")
        else:
            print("⚠️ No products found. Using manual fallback.")
            sku = "MANUAL-TEST-SKU"
            price = 100.0

        receipt_no = f"REC-SIM-{int(time.time())}"
        
        sale_payload = {
            "pos_device_id": "SIM-DEVICE-01",
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
        
        # 3. Execute Sale
        print(f"\n💳 Processing Sale ({receipt_no}) for {target_email}...")
        url = f"/api/pos/sales?customer_id={cust_id}&email={target_email}"
        
        res = await client.post(url, json=sale_payload)
        
        if res.status_code == 200:
            data = res.json()
            print(f"✅ Sale Successful!")
            print(f"📄 Receipt: {data['receipt_no']}")
            print(f"🎁 Points Earned: {data.get('points_earned', 0)}")
            print("\n📨 Email trigger should have happened in background.")
            print("ℹ️ Check your inbox for the receipt and QR code.")
        else:
            print(f"❌ Sale Failed: {res.status_code}")
            print(res.text)

if __name__ == "__main__":
    asyncio.run(simulate_sale_async())
