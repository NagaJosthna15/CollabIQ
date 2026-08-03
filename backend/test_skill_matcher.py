from services.matching.skill_matcher import (
    skill_match
)

required_skills = [
    "Python",
    "Machine Learning",
    "React",
    "MongoDB"
]

candidate_profile = {

    "skills": [
        "Python",
        "Machine Learning",
        "Power BI"
    ],

    "resume_skills": [
        "python",
        "react",
        "mongodb",
        "javascript"
    ]

}

score = skill_match(
    required_skills,
    candidate_profile
)

print(
    "Skill Score:",
    score
)