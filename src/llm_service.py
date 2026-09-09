import os
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


def analyze_incident(incident):
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

    return response.output_parsed