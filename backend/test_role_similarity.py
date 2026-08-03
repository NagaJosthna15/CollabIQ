from services.matching.semantic_role_matcher import (
    role_similarity
)

tests = [
    ("AI/ML Engineer", "AI Solutions Engineer"),
    ("Frontend Developer", "React Developer"),
    ("Backend Developer", "Spring Boot Developer"),
    ("Cloud Engineer", "AWS Engineer"),
    ("Data Engineer", "SQL Developer"),
]

for recruiter_role, candidate_role in tests:

    score = role_similarity(
        recruiter_role,
        candidate_role
    )

    print(
        recruiter_role,
        "<->",
        candidate_role,
        "=",
        score
    )