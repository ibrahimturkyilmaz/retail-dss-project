from fastapi.testclient import TestClient
from main import app
import datetime

client = TestClient(app)

def test_api():
    print("="*50)
    print("🚀 REFACTOR VERIFICATION WITH TESTCLIENT")
    print("="*50)
    
    endpoints = [
        ("GET", "/", None),
        ("GET", "/api/sales", None),
        ("GET", "/api/users/admin", None),
        ("GET", "/api/stores", None),
        ("GET", "/api/stores/1/inventory", None),
        ("GET", "/api/products", None),
        # ("POST", "/api/products/launch", {"name": "Test Prod", "category": "Test", "price": 10, "cost": 5}) 
    ]
    
    results = []
    
    for method, url, data in endpoints:
        try:
            if method == "GET":
                response = client.get(url)
            else:
                response = client.post(url, json=data)
                
            status_symbol = "✅" if response.status_code == 200 else "❌"
            print(f"{status_symbol} {method} {url:<30} | Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"   Error: {response.text[:200]}")
                results.append(False)
            else:
                results.append(True)
                
        except Exception as e:
            print(f"🔥 {method} {url:<30} | EXCEPTION: {e}")
            results.append(False)
            
    print("="*50)
    success_count = sum(results)
    print(f"SUMMARY: {success_count}/{len(endpoints)} Passed")
    
    if all(results):
        print("🎉 ALL SYSTEMS GO!")
    else:
        print("⚠️ SOME TESTS FAILED")

if __name__ == "__main__":
    test_api()
