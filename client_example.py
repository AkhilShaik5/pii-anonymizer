import requests

API_URL = "http://localhost:8000/anonymize"

payload = {
    "text": "Contact John Doe at john.doe@example.com or 555-123-4567.",
    "language": "en",
}

resp = requests.post(API_URL, json=payload)
print("Status:", resp.status_code)
print(resp.json())
