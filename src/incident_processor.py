import json


def load_incidents():
    with open("data/incidents.json", "r") as file:
        return json.load(file)


def calculate_priority(impact, urgency):
    if impact == 1 and urgency == 1:
        return "P1"
    elif impact <= 2 and urgency <= 2:
        return "P2"
    else:
        return "P3"


def normalize_incident(incident):
    return {
        "incident_id": incident["number"],
        "title": incident["short_description"],
        "description": incident["description"],
        "impact": incident["impact"],
        "urgency": incident["urgency"],
        "priority": calculate_priority(
            incident["impact"],
            incident["urgency"]
        )
    }


def save_incidents(incidents):
    with open("data/ai_triaged_incidents.json", "w") as file:
        json.dump(incidents, file, indent=4)