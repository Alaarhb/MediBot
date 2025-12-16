import requests
import json
import time

url = "http://127.0.0.1:5000/get_response"
headers = {"Content-Type": "application/json"}

# diverse set of queries including typos, variations, and missing intents
tests = [
    # Hospital/Location (Existing)
    "Find a hospital near Paris", 
    "is there any clinic in London",
    "paramedic nearby",
    
    # Drugs (Existing)
    "Tell me about Aspirin",
    "side effects of Tylenol",
    "is advil safe?",
    
    # Symptoms (Existing)
    "I have a fever",
    "my head hurts a lot",
    "stomach pain severe",
    
    # Mental Health (Existing)
    "I feel very sad",
    "panicking right now",
    
    # Gaps / Hard Queries (Likely Fail)
    "I twisted my ankle", # Injury
    "I have a burn on my hand", # Injury
    "my blood pressure is high", # Condition
    "diabetes symptoms", # Condition
    "can I book an appointment?", # Admin
    "what are your hours?", # Admin
    "who created you?", # Meta
    "I ate something bad", # Variation of stomach
    "my kid has a high temp", # Variation of fever
    "rash on leg", # Variation
]

print(f"Running {len(tests)} stress tests...")
files = 0
passes = 0

for msg in tests:
    try:
        response = requests.post(url, json={"message": msg}, headers=headers, timeout=5)
        res_json = response.json()
        reply = res_json.get("response", "")
        
        # Simple heuristic: if it contains "I'm sorry", it's a fallback (Fail for this test context)
        is_fallback = "I'm sorry, I didn't quite understand" in reply
        
        status = "FAIL" if is_fallback else "PASS"
        if not is_fallback:
            passes += 1
            
        print(f"[{status}] Query: '{msg}'")
        if is_fallback:
             print(f"       Reply: {reply[:60]}...")
             
    except Exception as e:
        print(f"[ERROR] {msg}: {e}")

print(f"\nScore: {passes}/{len(tests)} ({(passes/len(tests))*100:.1f}%)")
