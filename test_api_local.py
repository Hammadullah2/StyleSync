import requests
import json

url = "http://localhost:8000/chat"
payload = {"query": "red shoes"}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json()
        print("Response:", data['response'])
        print("\nRecommended Items:")
        for item in data['recommended_items']:
            print(f"- {item['productDisplayName']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Failed to connect: {e}")
