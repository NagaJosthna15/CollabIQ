from services.recruiter_agent import RecruiterAgent

agent = RecruiterAgent()

result = agent.understand_project(

    title="AI Healthcare Assistant",

    description="""
Build an AI-powered healthcare platform
that predicts diseases from symptoms,
stores patient history,
provides recommendations,
and has a React dashboard.
"""
)

print(result)