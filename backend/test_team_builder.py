from services.recruiter_agent import (
    RecruiterAgent
)


agent = RecruiterAgent()


result = agent.recruit_team(
    "AI Healthcare Assistant",
    """
    Build an AI healthcare platform
    using Python, React,
    Machine Learning,
    MongoDB and NLP.
    """
)


print(
    "\n========== PROJECT REQUIREMENTS ==========\n"
)

print(
    result[
        "project_requirements"
    ]
)

print(
    "\n========== FINAL TEAM ==========\n"
)

print(
    result[
        "final_team"
    ]
)


print(
    "\n========== FINAL COVERAGE ==========\n"
)

print(
    result[
        "coverage"
    ]
)


print(
    "\n========== SKILL GAPS ==========\n"
)

print(
    result[
        "skill_gaps"
    ]
)