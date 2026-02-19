import asyncio
from httpx import AsyncClient, ASGITransport
from main import app
import datetime

async def test_z_report():
    print("Testing Z-Report Endpoint...")
    
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        today = datetime.date.today().isoformat()
        
        payload = {
            "pos_device_id": "POS-TEST-Z",
            "z_no": "Z-9999",
            "date": today,
            "total_sales": 5000.0,
            "total_returns": 100.0,
            "total_cash": 4000.0,
            "total_credit": 900.0
        }

        # Mock Email
        email = "mock_test@example.com"
        
        try:
            print(f"Sending Z-Report for {email}...")
            response = await client.post(f"/api/pos/z-report?email={email}", json=payload)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Z-Report Created Successfully.")
                print("Response:", response.json())
            else:
                print(f"❌ Failed: {response.text}")
                
        except Exception as e:
             print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_z_report())
