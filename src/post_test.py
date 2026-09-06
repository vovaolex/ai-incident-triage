import requests


incident = {
    "number": "INC001004",
    "short_description": "Software installation failed",
    "description": "User cannot install Microsoft Teams",
    "impact": 3,
    "urgency": 2
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=incident
)

print(f"Status code: {response.status_code}")

if response.status_code == 201:
    result = response.json()
    print(result)
else:
    print("POST request failed.")