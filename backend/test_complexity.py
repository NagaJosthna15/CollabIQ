from services.project_intelligence import (
    calculate_complexity_score
)

readme = """
AI-powered team optimization platform.

Features:
- Resume Analysis
- Candidate Ranking
- GitHub Intelligence
- Team Matching

Tech Stack:
- FastAPI
- MongoDB
- Machine Learning
"""

score = calculate_complexity_score(
    readme
)

print(score)