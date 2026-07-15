from services.project_intelligence import model

text = """
AI-powered healthcare assistant
for disease prediction
"""

embedding = model.encode(text)

print(
    len(embedding)
)