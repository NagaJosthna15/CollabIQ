from services.recruiter_agent import RecruiterAgent


def main():

    agent = RecruiterAgent()

    result = agent.recruit_team(
        title="AI Healthcare Platform",
        description="""
Build an AI-powered healthcare platform with a frontend,
backend APIs, machine learning models, NLP capabilities,
cloud deployment, Docker, Kubernetes, security,
authentication, and HIPAA compliance.
"""
    )

    print("\n========== FINAL RESULT ==========\n")

    print("FINAL TEAM:")

    for member in result.get("final_team", []):

        profile = (
            member.get("candidate", {})
            .get("profile", {})
        )

        print(
            profile.get("student"),
            "-",
            profile.get("recommended_role")
        )

    print("\nCOVERAGE:")
    print(result.get("coverage"))

    print("\nADDITIONAL CANDIDATES:")

    additional = result.get(
        "additional_candidates",
        {}
    )

    candidates = additional.get(
        "recommended_candidates",
        []
    )

    if candidates:

        for candidate in candidates:

            print(
                candidate.get("student_name"),
                "-",
                candidate.get("recommended_role"),
                "| Score:",
                candidate.get("ranking_score")
            )

    else:

        print("No additional candidates selected.")

    print("\nADDITIONAL STATUS:")
    print(additional.get("status"))


if __name__ == "__main__":
    main()