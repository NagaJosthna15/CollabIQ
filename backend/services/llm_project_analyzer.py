from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
def analyze_project_with_llm(readme_text):

    prompt = f"""
    Analyze the following GitHub project README.

    Give response in JSON format:
    Return ONLY valid JSON.
    Do not provide explanations.
    Do not provide markdown.
    Do not write any text outside JSON.

    {{
        "project_summary": "...",
        "industry_impact": 0-100,
        "future_scope": 0-100,
        "innovation_level": "Low/Medium/High"
    }}

    README:

    {readme_text[:4000]}
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

    content = response.choices[0].message.content

    content = content.replace(
    "```json",
    ""
    ).replace(
    "```",
    ""
    ).strip()

    start = content.find("{")
    end = content.rfind("}")

    json_content = content[
    start:end+1
]

    return json.loads(
    json_content
)