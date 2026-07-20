from services.llm.llm_career_assessor import generate_career_assessment

profile = {
    "strong_domains": [
        "Artificial Intelligence",
        "Web Development",
        "Automation"
    ],
    "average_innovation": 17.7,
    "average_complexity": 26.08,
    "average_industry_impact": 55,
    "average_future_scope": 72,
    "recommended_role": "AI Solutions Engineer"
}

result = generate_career_assessment(profile)

print(result)