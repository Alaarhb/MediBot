import requests
import json

url = "http://127.0.0.1:5000/get_response"
headers = {"Content-Type": "application/json"}

tests = [
    "Find hospitals in Paris",
    "Find a hospital near Paris",
    "Hospitals in London",
    "Tell me about Aspirin",
    "Hello"
]

for msg in tests:
    print(f"Testing: {msg}")
    try:
        response = requests.post(url, json={"message": msg}, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        # Use repr to avoid encoding errors in console
        print(f"Response: {json.dumps(response.json(), ensure_ascii=True)}") 
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)
