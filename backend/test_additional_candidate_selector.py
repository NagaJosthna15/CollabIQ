from services.team_builder.additional_candidate_selector import (
    AdditionalCandidateSelector
)

from services.recruiter_agent import RecruiterAgent


def normalize_name(name):
    if not name:
        return ""

    return "".join(
        str(name).lower().split()
    )


def main():

    agent = RecruiterAgent()

    students = agent.build_student_profiles()

    if not students:
        print("No student profiles were returned.")
        return

    print("\n========== ALL STUDENTS ==========\n")

    for student in students:
        print(
            student.get("student", ""),
            student.get("skills", []),
            student.get("recommended_role", "")
        )

    current_team_names = {
        normalize_name("Jyoshna"),
        normalize_name("Ananya Singh")
    }

    current_team = [
        student
        for student in students
        if normalize_name(
            student.get("student", "")
        ) in current_team_names
    ]

    available_candidates = [
        student
        for student in students
        if normalize_name(
            student.get("student", "")
        ) not in current_team_names
    ]

    print("\n========== CURRENT TEAM ==========\n")

    for student in current_team:
        print(
            f"Student: {student.get('student', '')}"
        )

        print(
            f"Recommended Role: "
            f"{student.get('recommended_role', '')}"
        )

        print(
            f"Skills: "
            f"{student.get('skills', [])}"
        )

        print(
            f"Resume Skills: "
            f"{student.get('resume_skills', [])}"
        )

        print("----------------------------------")

    project_requirements = {
        "skills": [
            "React",
            "TypeScript",
            "JavaScript",
            "HTML",
            "CSS",
            "Python",
            "FastAPI",
            "Flask",
            "REST API",
            "MongoDB",
            "Machine Learning",
            "TensorFlow",
            "PyTorch",
            "scikit-learn",
            "NLP",
            "Hugging Face Transformers",
            "Docker",
            "Kubernetes",
            "CI/CD",
            "GitHub Actions",
            "AWS",
            "Azure",
            "GCP",
            "JWT",
            "OAuth2",
            "HIPAA",
            "Security"
        ],

        "roles": [
            "Frontend Engineer",
            "Backend Engineer",
            "Machine Learning Engineer",
            "NLP Engineer",
            "DevOps Engineer",
            "Cloud Engineer",
            "Security Engineer",
            "Compliance Engineer"
        ]
    }

    selector = AdditionalCandidateSelector()

    result = selector.select_candidates(
        project_requirements,
        current_team,
        available_candidates,
        4
    )

    print(
        "\n========== ADDITIONAL CANDIDATE SELECTION ==========\n"
    )

    print(
        "Number Requested:",
        result.get(
            "number_requested",
            4
        )
    )

    print("\nMissing Skills:")

    for skill in result.get(
        "missing_skills",
        []
    ):
        print(f"- {skill}")

    print("\nMissing Roles:")

    for role in result.get(
        "missing_roles",
        []
    ):
        print(f"- {role}")

    recommendations = result.get(
        "recommended_candidates",
        []
    )

    print("\nRecommended Candidates:\n")

    if not recommendations:
        print(
            "No suitable candidates found."
        )

    for index, candidate in enumerate(
        recommendations,
        start=1
    ):

        print(f"#{index}")

        print(
            "Student:",
            candidate.get(
                "student_name",
                ""
            )
        )

        print(
            "Overall Score:",
            candidate.get(
                "overall_score",
                0
            )
        )

        print(
            "Matched Skill:",
            candidate.get(
                "matched_skill"
            ) or "None"
        )

        print(
            "Skill Similarity:",
            candidate.get(
                "skill_similarity",
                0
            )
        )

        print(
            "Matched Role:",
            candidate.get(
                "matched_role"
            ) or "None"
        )

        print(
            "Role Similarity:",
            candidate.get(
                "role_similarity",
                0
            )
        )

        print(
            "Ranking Score:",
            candidate.get(
                "ranking_score",
                0
            )
        )

        print(
            "Recommended Role:",
            candidate.get(
                "recommended_role",
                ""
            )
        )

        print("----------------------------------")

    print(
        "\n========== SELECTION ROUNDS ==========\n"
    )

    rounds = result.get(
        "selection_rounds",
        []
    )

    if not rounds:
        print(
            "No selection rounds completed."
        )

    for round_data in rounds:

        print(
            "Round:",
            round_data.get(
                "round",
                ""
            )
        )

        print(
            "Selected:",
            round_data.get(
                "selected_student",
                ""
            )
        )

        print(
            "Score:",
            round_data.get(
                "score",
                0
            )
        )

        print(
            "Matched Skill:",
            round_data.get(
                "matched_skill"
            ) or "None"
        )

        print(
            "Matched Role:",
            round_data.get(
                "matched_role"
            ) or "None"
        )

        print("----------------------------------")

    print(
        "\n========== REMAINING GAPS ==========\n"
    )

    print("Remaining Skills:")

    for skill in result.get(
        "remaining_skills",
        []
    ):
        print(f"- {skill}")

    print("\nRemaining Roles:")

    for role in result.get(
        "remaining_roles",
        []
    ):
        print(f"- {role}")

    print(
        "\n========== SELECTION SUMMARY ==========\n"
    )

    print(
        "Current Team Size:",
        len(current_team)
    )

    print(
        "Additional Members Requested:",
        result.get(
            "number_requested",
            4
        )
    )

    print(
        "Recommended Members:",
        result.get(
            "recommended_members",
            0
        )
    )

    print(
        "Remaining Members Needed:",
        result.get(
            "remaining_members_needed",
            0
        )
    )

    print(
        "Status:",
        result.get(
            "status",
            "unknown"
        )
    )

    print(
        "\n=======================================\n"
    )


if __name__ == "__main__":
    main()