from services.project_intelligence import (
    calculate_innovation_score
)

readme = """
AI-powered team optimization platform.

Features:
- Resume Analysis
- Candidate Ranking
- Team Matching
- GitHub Intelligence
"""

score = calculate_innovation_score(
    readme
)

print(score)