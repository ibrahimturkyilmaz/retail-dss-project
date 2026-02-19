from fastapi.testclient import TestClient
import inspect

try:
    print(f"Signature: {inspect.signature(TestClient.__init__)}")
except Exception as e:
    print(f"Error inspecting signature: {e}")

print(f"TestClient module: {TestClient.__module__}")
