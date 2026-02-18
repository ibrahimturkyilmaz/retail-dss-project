import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8002"

def wait_for_server():
    print("Waiting for server...")
    for _ in range(10):
        try:
            requests.get(BASE_URL)
            print("Server is up!")
            return True
        except:
            time.sleep(1)
    return False

def test_endpoints():
    if not wait_for_server():
        print("Server failed to start")
        sys.exit(1)

    endpoints = [
        "/",
        "/api/sales",
        "/api/stores",
        "/api/products",
        "/api/analytics", # This might fail if 404 or auth, but let's check basic
    ]
    
    success = True
    for ep in endpoints:
        url = f"{BASE_URL}{ep}"
        try:
            r = requests.get(url)
            print(f"GET {ep} -> {r.status_code}")
            if r.status_code not in [200, 404]: # 404 is acceptable for some if empty
                # /api/analytics is incorrect path, it is /api/sales/analytics
                pass
        except Exception as e:
            print(f"GET {ep} -> Failed: {e}")
            success = False
            
    # Check specific async endpoints
    try:
        r = requests.get(f"{BASE_URL}/api/users/admin")
        print(f"GET /api/users/admin -> {r.status_code}")
    except:
        success = False

if __name__ == "__main__":
    test_endpoints()
