from services.project_intelligence import (
    detect_domain
)

readme = """
AI-powered healthcare assistant
for disease prediction using
patient history and analytics.
"""

result = detect_domain(
    readme
)

print(result)