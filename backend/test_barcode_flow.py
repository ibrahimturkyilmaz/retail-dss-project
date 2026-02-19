import asyncio
from httpx import AsyncClient, ASGITransport
from main import app

async def test_barcode_flow():
    print("Testing Barcode Scanning Flow...")
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Test a known barcode (e.g., from our script logic)
        # We know we assigned sequential codes starting 8690000000001
        test_barcode = "8690000000001" 
        
        print(f"\n1. Scanning Barcode: {test_barcode}")
        res = await client.get(f"/api/pos/products/scan/{test_barcode}")
        
        if res.status_code == 200:
            product = res.json()
            print(f"✅ Product Found: {product['name']} (SKU: {product['sku']}) - Price: {product['price']}")
            
            # 2. Verify SKU matches barcode
            if product['sku'] == test_barcode:
                 print("✅ SKU matches query.")
            else:
                 print(f"❌ SKU mismatch! Expected {test_barcode}, got {product['sku']}")
        else:
            print(f"❌ Scan Failed: {res.text}")

        # 3. Test Invalid Barcode
        invalid_code = "000000"
        print(f"\n2. Scanning Invalid Barcode: {invalid_code}")
        res = await client.get(f"/api/pos/products/scan/{invalid_code}")
        if res.status_code == 404:
             print("✅ Correctly returned 404 for invalid barcode.")
        else:
             print(f"❌ Expected 404, got {res.status_code}")

if __name__ == "__main__":
    asyncio.run(test_barcode_flow())
