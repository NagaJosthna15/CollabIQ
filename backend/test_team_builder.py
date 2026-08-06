from services.recruiter_agent import RecruiterAgent

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

print(result)