import json
from .client import client


def analyze_project_requirements(title, description):

    prompt = f"""
You are a Senior Technical Architect and AI Project Manager.

Analyze the following software project.

Project Title:
{title}

Project Description:
{description}

Your task:

1. Understand the project.
2. Identify all important technical domains.
3. Extract required technical skills.
4. Estimate project difficulty.
5. Suggest an ideal team size.
6. Suggest the roles required.
7. Mention optional skills that would make the team stronger.

Return ONLY valid JSON.

Return exactly this format:

{{
    "project_summary": "...",

    "project_domains": [
        "...",
        "..."
    ],

    "required_skills": [
        "...",
        "..."
    ],

    "optional_skills": [
        "...",
        "..."
    ],

    "difficulty": "Low | Medium | High",

    "estimated_team_size":
     - Small project: 2–4 members
- Medium project: 4–6 members
- Large enterprise project: 6–8 members

Choose the smallest team capable of successfully completing the project.


    "preferred_roles": [
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
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    start = content.find("{")
    end = content.rfind("}") + 1

    try:
        return json.loads(content[start:end])

    except Exception:

        return {
            "project_summary": "",
            "project_domains": [],
            "required_skills": [],
            "optional_skills": [],
            "difficulty": "Unknown",
            "estimated_team_size": 0,
            "preferred_roles": []
        }