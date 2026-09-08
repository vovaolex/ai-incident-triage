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
    # print incident number
    print(f"INC: {incident["number"]}")
    # print category
    print(f"Category: {result.category}")
    # print summary
    print(f"Summary: {result.summary}")
    # loop through recommended actions
    for action in result.recommended_actions:
        print(f"- {action}")