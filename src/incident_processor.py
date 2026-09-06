import json
import requests


def load_incidents():
    with open("data/incidents.json", "r") as file:
        incidents = json.load(file)

    return incidents

def calculate_priority(impact, urgency):
    if impact == 1 and urgency == 1:
        return "P1"
    elif impact <= 2 and urgency <= 2:
        return "P2"
    else:
        return "P3"

def normalize_incident(incident):
    normalized_incident = {
        "incident_id": incident["number"],
        "title": incident["short_description"],
        "description": incident["description"],
        "impact": incident["impact"],
        "urgency": incident["urgency"],
        "priority": calculate_priority(incident["impact"], incident["urgency"])
    }

    return normalized_incident

def save_incidents(incidents):
    with open("data/normalized_incidents.json", "w") as file:
        json.dump(incidents, file, indent=4)

def send_incident(incident):
    try:
        response = requests.post(
            "https://jsonplaceholder.typicode.com/posts",
            json=incident,
            timeout=10
        )

        if response.status_code == 201:
            return response.json()
        else:
            print(f"API reuturned status code: {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
        return None
    
incidents = load_incidents()

normalized_incidents = []

for incident in incidents:
    normalized_incident = normalize_incident(incident)
    normalized_incidents.append(normalized_incident)
    result = send_incident(normalized_incident)
    print(result)

save_incidents(normalized_incidents)

print("Incidents normalized and saved successfully")