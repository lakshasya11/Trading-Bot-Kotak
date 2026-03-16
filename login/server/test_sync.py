import requests

# Test PC2 endpoint
pc2_url = 'http://192.168.0.104:5004/api/sync-signup'

test_data = {
    'client_id': 'TEST001',
    'username': 'test_user',
    'email': 'test@example.com',
    'phone': '9999999999',
    'aadhar': '123456789012',
    'qr_key': 'TESTQRKEY123'
}

print("Testing PC2 sync endpoint...")
print(f"URL: {pc2_url}")
print(f"Data: {test_data}")

try:
    response = requests.post(pc2_url, json=test_data, timeout=5)
    print(f"\n✓ Response: {response.status_code}")
    print(f"✓ Body: {response.json()}")
except Exception as e:
    print(f"\n✗ Error: {e}")
