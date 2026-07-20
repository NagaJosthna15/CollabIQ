import json
from .client import client


def generate_career_assessment(profile):

    prompt = f"""
You are a Senior AI Career Mentor, Technical Recruiter.

Analyze the following student's profile thoroughly.

Student Profile:
{json.dumps(profile, indent=2)}

Evaluate the student using these factors:
- Strong technical domains
- Innovation score
- Project complexity score
- Industry impact
- Future scope
- Recommended role

Guidelines:
- Do NOT give generic advice.
- Explain WHY the student received the overall rating.
- Use the provided metrics while reasoning.
- Identify the student's strongest technical abilities.
- Recommend suitable career paths.
- Recommend real-world projects that will strengthen the profile.
- Recommend technologies and skills to learn next.
- Keep the response professional and personalized.
- Return ONLY valid JSON.
- Do NOT include markdown or explanations outside the JSON.

Return exactly this JSON structure:

{{
  "overall_rating": "...",
  "reason": "...",
  "strengths": [
    "...",
    "..."
  ],
  "growth_areas": [
    "...",
    "..."
  ],
  "career_advice": "...",
  "recommended_projects": [
    "...",
    "...",
    "..."
  ],
  "next_learning_path": [
    "...",
    "...",
    "..."
  ]
}}
"""


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    try:
        start = content.find("{")
        end = content.rfind("}") + 1

        return json.loads(content[start:end])

    except Exception:
        return {
        "overall_rating": "Unavailable",
        "reason": "The AI could not generate a valid assessment.",
        "strengths": [],
        "growth_areas": [],
        "career_advice": "",
        "recommended_projects": [],
        "next_learning_path": []
    }