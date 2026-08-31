import json
import re
import time
from .client import client


def generate_career_assessment(profile):
    prompt = f"""
You are a Senior AI Career Mentor and Technical Recruiter.

Analyze the following student's profile thoroughly.

Student Profile:
{json.dumps(profile, indent=2, default=str)}

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
- Do NOT include markdown.
- Do NOT include explanations outside the JSON.
- All keys and string values must use valid JSON double quotes.
- Do not use trailing commas.

Return exactly this JSON structure:

{{
  "overall_rating": "string",
  "reason": "string",
  "strengths": ["string"],
  "growth_areas": ["string"],
  "career_advice": "string",
  "recommended_projects": ["string"],
  "next_learning_path": ["string"]
}}
"""

    last_error = None

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_completion_tokens=1200
            )

            content = response.choices[0].message.content

            if not content:
                raise ValueError("Empty response from AI")

            content = content.strip()

            content = re.sub(
                r"^```(?:json)?\s*|\s*```$",
                "",
                content,
                flags=re.IGNORECASE
            ).strip()

            start = content.find("{")
            end = content.rfind("}")

            if start == -1 or end == -1 or end <= start:
                raise ValueError("No valid JSON object found")

            json_content = content[start:end + 1]

            json_content = re.sub(r",\s*}", "}", json_content)
            json_content = re.sub(r",\s*]", "]", json_content)

            result = json.loads(json_content)

            return {
                "overall_rating": result.get("overall_rating", "Unavailable"),
                "reason": result.get("reason", ""),
                "strengths": result.get("strengths", []),
                "growth_areas": result.get("growth_areas", []),
                "career_advice": result.get("career_advice", ""),
                "recommended_projects": result.get("recommended_projects", []),
                "next_learning_path": result.get("next_learning_path", [])
            }

        except Exception as e:
            last_error = e

            if attempt < 2:
                time.sleep(2 * (attempt + 1))

    print(f"Career assessment generation error: {last_error}")

    return {
        "overall_rating": "Unavailable",
        "reason": "The AI could not generate a valid assessment.",
        "strengths": [],
        "growth_areas": [],
        "career_advice": "",
        "recommended_projects": [],
        "next_learning_path": []
    }