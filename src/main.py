from incident_processor import (
    load_incidents,
    normalize_incident,
    save_incidents
)

from llm_service import analyze_incident


incidents = load_incidents()

enriched_incidents = []

for incident in incidents:
    normalized_incident = normalize_incident(incident)

    ai_analysis = analyze_incident(incident)

    enriched_incident = {
        **normalized_incident,
        "ai_category": ai_analysis.category,
        "ai_summary": ai_analysis.summary,
        "probable_cause": ai_analysis.probable_cause,
        "recommended_actions": ai_analysis.recommended_actions
    }

    enriched_incidents.append(enriched_incident)

    print(f"Processed {incident['number']}")


save_incidents(enriched_incidents)

print("AI triage completed and saved.")