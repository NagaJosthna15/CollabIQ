from services.recruiter_agent import RecruiterAgent
from services.team_builder.additional_candidate_selector import AdditionalCandidateSelector
from services.ranking.candidate_ranker import rank_candidates


agent = RecruiterAgent()

requirements = agent.understand_project(
    "AI Powered Healthcare Management System",
    """
    Build an AI-powered healthcare management platform that helps
    hospitals manage patient data, appointments, medical records,
    healthcare analytics, and intelligent recommendations.

    The system should include a React frontend, Python backend APIs,
    MongoDB database, machine learning and NLP capabilities,
    REST APIs, authentication, Docker, CI/CD, cloud deployment,
    healthcare data privacy, and HIPAA compliance.
    """
)

student_profiles = agent.build_student_profiles()

selected_team = [
    profile
    for profile in student_profiles
    if profile.get("student") in [
        "Jyoshna",
        "Ananya Singh"
    ]
]

print("\n========== CURRENT TEAM ==========\n")

for member in selected_team:

    print(
        f"Student: {member.get('student')}"
    )

    print(
        f"Recommended Role: {member.get('recommended_role', '')}"
    )

    print(
        f"Skills: {member.get('skills', [])}"
    )

    print(
        f"Resume Skills: {member.get('resume_skills', [])}"
    )

    print(
        "----------------------------------"
    )


ranked_candidates = rank_candidates(
    requirements,
    student_profiles
)


selector = AdditionalCandidateSelector()


result = selector.select_candidates(
    project_requirements=requirements,
    student_profiles=student_profiles,
    selected_team=selected_team,
    ranked_candidates=ranked_candidates,
    number_needed=4
)


print(
    "\n========== ADDITIONAL CANDIDATE SELECTION ==========\n"
)


print(
    f"Number Requested: {result['number_requested']}"
)


print("\nMissing Skills:")

missing_skills = requirements.get(
    "required_skills",
    []
)

if missing_skills:

    for skill in missing_skills:

        print(
            f"- {skill}"
        )

else:

    print(
        "- No missing skills"
    )


print("\nMissing Roles:")

missing_roles = requirements.get(
    "preferred_roles",
    []
)

if missing_roles:

    for role in missing_roles:

        print(
            f"- {role}"
        )

else:

    print(
        "- No missing roles"
    )


print("\nRecommended Candidates:\n")


recommended_candidates = result.get(
    "recommended_candidates",
    []
)


if recommended_candidates:

    for index, candidate in enumerate(
        recommended_candidates,
        start=1
    ):

        print(
            f"#{index}"
        )

        print(
            f"Student: {candidate.get('student')}"
        )

        print(
            f"Overall Score: {candidate.get('score', 0)}"
        )

        print(
            f"Matched Skill: {candidate.get('matched_skill')}"
        )

        print(
            f"Skill Similarity: {candidate.get('skill_similarity', 0)}"
        )

        print(
            f"Matched Role: {candidate.get('matched_role')}"
        )

        print(
            f"Role Similarity: {candidate.get('role_similarity', 0)}"
        )

        print(
            f"Ranking Score: {candidate.get('ranking_score', 0)}"
        )

        print(
            f"Recommended Role: {candidate.get('recommended_role', '')}"
        )

        print(
            "----------------------------------"
        )

else:

    print(
        "No suitable candidates found."
    )


print(
    "\n========== SELECTION ROUNDS ==========\n"
)


selection_rounds = result.get(
    "selection_rounds",
    []
)


if selection_rounds:

    for selection_round in selection_rounds:

        print(
            f"Round: {selection_round.get('round')}"
        )

        print(
            f"Selected: {selection_round.get('student')}"
        )

        print(
            f"Score: {selection_round.get('score', 0)}"
        )

        print(
            f"Matched Skill: {selection_round.get('matched_skill')}"
        )

        print(
            f"Matched Role: {selection_round.get('matched_role')}"
        )

        print(
            "----------------------------------"
        )

else:

    print(
        "No selection rounds completed."
    )


print(
    "\n========== REMAINING GAPS ==========\n"
)


print("Remaining Skills:")


remaining_skills = result.get(
    "remaining_skills",
    []
)


if remaining_skills:

    for skill in remaining_skills:

        print(
            f"- {skill}"
        )

else:

    print(
        "- No remaining skills"
    )


print("\nRemaining Roles:")


remaining_roles = result.get(
    "remaining_roles",
    []
)


if remaining_roles:

    for role in remaining_roles:

        print(
            f"- {role}"
        )

else:

    print(
        "- No remaining roles"
    )


print(
    "\n========== SELECTION SUMMARY ==========\n"
)


print(
    f"Current Team Size: {len(selected_team)}"
)

print(
    f"Additional Members Requested: {result['number_requested']}"
)

print(
    f"Recommended Members: {result['recommended_members']}"
)

print(
    f"Remaining Members Needed: {result['remaining_members_needed']}"
)

print(
    f"Status: {result['status']}"
)


print(
    "\n=======================================\n"
)