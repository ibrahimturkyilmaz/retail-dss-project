import requests
import json

# Setup
API_URL = "http://localhost:8001"

def test_proximity():
    print("📍 Testing Geofence Proximity...")
    
    # Coordinates for "Nişantaşı" or central Istanbul
    lat = 41.05
    lon = 28.99
    
    payload = {
        "lat": lat,
        "lon": lon,
        "customer_id": 32 # Assuming 'kemal.yildiz' or similar exists
    }
    
    try:
        response = requests.post(f"{API_URL}/api/marketing/check-proximity", json=payload)
        
        print(f"Status: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_proximity()
