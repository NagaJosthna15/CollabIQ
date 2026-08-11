from services.student_service import get_all_students

from services.team_builder.skill_gap_resolver import (
    SkillGapResolver
)


# -----------------------------------------
# Get all students
# -----------------------------------------

students = get_all_students()


# -----------------------------------------
# Example selected team
# -----------------------------------------

selected_team = [

    {
        "role": "Senior Technical Architect",

        "candidate": {
            "profile": {
                "student": "Jyoshna"
            }
        }
    },

    {
        "role": "AI/ML Engineer",

        "candidate": {
            "profile": {
                "student": "Ananya Singh"
            }
        }
    }
]


# -----------------------------------------
# Missing skills detected by
# Coverage Analyzer
# -----------------------------------------

missing_skills = [
    "NLP"
]


# -----------------------------------------
# Create resolver
# -----------------------------------------

resolver = SkillGapResolver()


# -----------------------------------------
# Find candidates
# -----------------------------------------

recommendations = resolver.find_candidates(
    missing_skills,
    students,
    selected_team
)


# -----------------------------------------
# Print results
# -----------------------------------------

print(
    "\n========== SKILL GAP RESOLUTION ==========\n"
)


for recommendation in recommendations:

    print(
        "Missing Skill:",
        recommendation["missing_skill"]
    )

    candidates = recommendation[
        "candidates"
    ]

    if not candidates:

        print(
            "No suitable candidate found."
        )

    else:

        for candidate in candidates:

            print(
                "Candidate:",
                candidate["student"]
            )

            print(
                "Matched Skill:",
                candidate["matched_skill"]
            )

            print(
                "Similarity:",
                candidate["similarity"]
            )

            print(
                "-----------------------------------"
            )


print(
    "\n===========================================\n"
)