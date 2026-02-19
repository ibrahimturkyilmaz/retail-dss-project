
import sys
import os
from fastapi.testclient import TestClient

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from main import app

client = TestClient(app)

def test_find_nearby_store():
    # Istanbul coordinates
    payload = {
        "lat": 41.0082,
        "lon": 28.9784
    }
    
    print(f"📍 Testing /api/simulate/find-nearby-store with {payload}...")
    
    response = client.post("/api/simulate/find-nearby-store", json=payload)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            print("❌ API returned error.")
        else:
            print(f"✅ Success! Found store: {data.get('name')} at {data.get('distance_km')} km.")
    else:
        print("❌ Request failed.")

if __name__ == "__main__":
    test_find_nearby_store()
