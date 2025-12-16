import requests
import json

url = "http://127.0.0.1:5000/get_response"
headers = {"Content-Type": "application/json"}

queries = [
    "jaw pain",
    "body on fire",
    "sup",
    "walk-in clinic",
    "visual aura",
    "dosage for advil"
]

for q in queries:
    try:
        response = requests.post(url, json={"message": q}, headers=headers, timeout=5)
        print(f"Query: {q}")
        print(f"Response: {response.json().get('response')}\n")
    except Exception as e:
        print(f"Error: {e}")
