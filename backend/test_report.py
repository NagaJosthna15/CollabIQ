from services.project_intelligence import (
    analyze_project
)

readme = """
CollabIQ is an AI-powered
team optimization platform.

Features:
- Resume Parsing
- GitHub Analysis
- Candidate Ranking
- Team Matching

Tech Stack:
- FastAPI
- MongoDB
- Machine Learning
"""

report = analyze_project(
    readme
)

print(report)