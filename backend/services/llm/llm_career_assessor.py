import json
import re
import time
from .client import client


MODEL_NAME = "openai/gpt-oss-120b"


def _fallback_assessment():
    return {
        "overall_rating": "Unavailable",
        "reason": "The AI could not generate a career assessment at this time.",
        "strengths": [],
        "growth_areas": [],
        "career_advice": "",
        "recommended_projects": [],
        "next_learning_path": []
    }


def _parse_json_response(content):
    if not content:
        raise ValueError("Empty response from AI")

    content = content.strip()

    # Remove markdown code fences if present
    content = re.sub(
        r"^```(?:json)?\s*",
        "",
        content,
        flags=re.IGNORECASE
    )

    content = re.sub(
        r"\s*```$",
        "",
        content,
        flags=re.IGNORECASE
    ).strip()

    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("No valid JSON object found")

    json_content = content[start:end + 1]

    # Remove trailing commas
    json_content = re.sub(
        r",\s*}",
        "}",
        json_content
    )

    json_content = re.sub(
        r",\s*]",
        "]",
        json_content
    )

    return json.loads(json_content)


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

    try:

        response = client.chat.completions.create(
            model=MODEL_NAME,
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

        result = _parse_json_response(content)

        return {
            "overall_rating": result.get(
                "overall_rating",
                "Unavailable"
            ),
            "reason": result.get(
                "reason",
                ""
            ),
            "strengths": result.get(
                "strengths",
                []
            ),
            "growth_areas": result.get(
                "growth_areas",
                []
            ),
            "career_advice": result.get(
                "career_advice",
                ""
            ),
            "recommended_projects": result.get(
                "recommended_projects",
                []
            ),
            "next_learning_path": result.get(
                "next_learning_path",
                []
            )
        }

    except Exception as e:

        error_text = str(e)

        # -----------------------------------------
        # RATE LIMIT HANDLING
        # -----------------------------------------

        if (
            "429" in error_text
            or "rate_limit" in error_text.lower()
            or "tokens per day" in error_text.lower()
            or "tokens per minute" in error_text.lower()
        ):
            print(
                "Career assessment skipped: "
                "LLM rate limit reached."
            )

            return _fallback_assessment()

        # -----------------------------------------
        # OTHER ERRORS
        # -----------------------------------------

        print(
            f"Career assessment generation error: {e}"
        )

        return _fallback_assessment()