from services.matching.semantic_role_matcher import (
    skill_similarity
)


test_cases = [

    (
        "Python programming",
        "Python"
    ),

    (
        "React framework",
        "React"
    ),

    (
        "Machine Learning algorithms",
        "Machine Learning"
    ),

    (
        "MongoDB database management",
        "MongoDB"
    ),

    (
        "NLP techniques",
        "React"
    )
]


print(
    "\n========== SKILL SIMILARITY TEST ==========\n"
)


for required_skill, candidate_skill in test_cases:

    score = skill_similarity(
        required_skill,
        candidate_skill
    )

    print(
        required_skill,
        "<->",
        candidate_skill,
        "| Similarity:",
        score
    )


print(
    "\n===========================================\n"
)