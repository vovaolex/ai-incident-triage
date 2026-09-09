import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class IncidentAnalysis(BaseModel):
    category: str
    summary: str
    probable_cause: str
    recommended_actions: list[str]


with open("data/incidents.json", "r") as file:
    incidents = json.load(file)

enriched_incidents = []

for incident in incidents:
    # call LLM
    response = client.responses.parse(
    model="gpt-5.6-luna",
    input=[
        {
            "role": "system",
            "content": "You are an IT incident triage assistant."
        },
        {
            "role": "user",
            "content": f"""
        Analyze this incident:

        Title: {incident["short_description"]}
        Description: {incident["description"]}
        Impact: {incident["impact"]}
        Urgency: {incident["urgency"]}

        Identify the category, summarize the issue, determine the probable cause,
        and provide 3 recommended troubleshooting actions.
        """
        }
    ],
    text_format=IncidentAnalysis
)
    # get result
    result = response.output_parsed
    ai_analysis = {
    "ai_category": result.category,
    "ai_summary": result.summary,
    "probable_cause": result.probable_cause,
    "recommended_actions": result.recommended_actions
}
    enriched_incident = {
    "number": incident["number"],
    "short_description": incident["short_description"],
    "description": incident["description"],
    "impact": incident["impact"],
    "urgency": incident["urgency"],
    **ai_analysis
}
    enriched_incidents.append(enriched_incident)
    print(f"Processed {incident['number']}")

with open("data/ai_triaged_incidents.json", "w") as file:
    json.dump(enriched_incidents, file, indent=4)

print("AI triage completed and saved.")