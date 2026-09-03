from services.recruiter_agent import RecruiterAgent


def main():

    agent = RecruiterAgent()

    title = "AI Powered Healthcare Platform"

    description = """
    Build an AI-powered healthcare platform that provides
    intelligent patient support and predictive analytics.

    The system should include:

    - React frontend
    - FastAPI backend
    - REST APIs
    - Machine Learning models
    - NLP capabilities
    - Hugging Face Transformers
    - MongoDB database
    - Docker containerization
    - Kubernetes deployment
    - CI/CD pipelines
    - GitHub Actions
    - AWS cloud deployment
    - Authentication using JWT and OAuth2
    - HIPAA compliance
    - Security implementation

    Required team roles:

    - Frontend Engineer
    - Backend Engineer
    - Machine Learning Engineer
    - NLP Engineer
    - DevOps Engineer
    - Cloud Engineer
    - Security Engineer
    - Compliance Engineer
    """

    print("\n")
    print("=" * 60)
    print("RECRUITER AGENT END-TO-END TEST")
    print("=" * 60)

    result = agent.recruit_team(
        title,
        description
    )

    print("\n========== PROJECT REQUIREMENTS ==========\n")

    requirements = result.get(
        "project_requirements",
        {}
    )

    print(requirements)

    print("\n========== FINAL TEAM ==========\n")

    final_team = result.get(
        "final_team",
        []
    )

    for member in final_team:

        profile = member.get(
            "candidate",
            {}
        ).get(
            "profile",
            {}
        )

        print(
            "Student:",
            profile.get("student")
        )

        print(
            "Primary Role:",
            member.get("role")
        )

        print(
            "Recommended Role:",
            profile.get("recommended_role")
        )

        print(
            "Selection Score:",
            member.get("selection_score")
        )

        print("-" * 40)

    print("\n========== ADDITIONAL CANDIDATES ==========\n")

    additional_candidates = result.get(
        "additional_candidates",
        []
    )

    if additional_candidates:

        for index, candidate in enumerate(
            additional_candidates,
            start=1
        ):

            print(f"#{index}")

            print(
                "Student:",
                candidate.get("student_name")
            )

            print(
                "Recommended Role:",
                candidate.get("recommended_role")
            )

            print(
                "Matched Skill:",
                candidate.get("matched_skill")
            )

            print(
                "Matched Role:",
                candidate.get("matched_role")
            )

            print(
                "Ranking Score:",
                candidate.get("ranking_score")
            )

            print("-" * 40)

    else:

        print(
            "No additional candidates were recommended."
        )

    print("\n========== COVERAGE ==========\n")

    coverage = result.get(
        "coverage",
        {}
    )

    print(
        "Missing Roles:",
        coverage.get("missing_roles", [])
    )

    print(
        "Missing Skills:",
        coverage.get("missing_skills", [])
    )

    print("\n========== TEST COMPLETED ==========\n")


if __name__ == "__main__":
    main()