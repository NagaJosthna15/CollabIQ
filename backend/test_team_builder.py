from services.recruiter_agent import RecruiterAgent
from services.team_builder.team_builder import assign_primary_roles

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
result = assign_primary_roles(
    result["project_requirements"],
    result["ranked_candidates"]
)

print(result)

