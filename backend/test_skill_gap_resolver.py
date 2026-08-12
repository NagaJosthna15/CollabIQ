from services.student_service import get_all_students

from services.team_builder.skill_gap_resolver import (
    SkillGapResolver
)


students = get_all_students()
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

missing_skills = [
    "NLP"
]

resolver = SkillGapResolver()
recommendations = resolver.find_candidates(
    missing_skills,
    students,
    selected_team
)

print(
    "\n========== SKILL GAP RESOLUTION ==========\n"
)


for recommendation in recommendations:

    print(
        "Missing Skill:",
        recommendation["missing_skill"]
    )

    print(
        "Status:",
        recommendation["status"]
    )

    print(
        "Genuine Skill Gap:",
        recommendation["is_genuine_gap"]
    )

    print(
        "Best Candidate:",
        recommendation["best_candidate"]
    )

    print(
        "Recommendation:",
        recommendation["recommendation"]
    )

    print(
        "\nAll Candidates:"
    )

    if recommendation["candidates"]:

        for candidate in recommendation["candidates"]:

            print(
                "  Student:",
                candidate["student"]
            )

            print(
                "  Matched Skill:",
                candidate["matched_skill"]
            )

            print(
                "  Similarity:",
                candidate["similarity"]
            )

    else:

        print(
            "  No suitable candidate found."
        )

    print(
        "-------------------------------------------"
    )


print(
    "\n===========================================\n"
)