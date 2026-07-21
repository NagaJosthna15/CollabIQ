from services.llm.llm_requirement_analyzer import (
    analyze_project_requirements
)

title = "AI Healthcare Assistant"

description = """
Build an AI-powered healthcare platform that predicts diseases
using patient symptoms, provides health recommendations,
stores patient history securely, and offers a React dashboard
for doctors and patients.
"""

result = analyze_project_requirements(
    title,
    description
)

print(result)