from services.recruiter_agent import RecruiterAgent
from services.team_builder.coverage_analyzer import (
    CoverageAnalyzer
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

final_team = result["final_team"]

analyzer = CoverageAnalyzer()

coverage = analyzer.analyze(
    result["project_requirements"],
    final_team
)

print("\n========== COVERAGE ANALYSIS ==========")

print(
    "Required Roles:",
    coverage["required_roles"]
)

print(
    "Covered Roles:",
    coverage["covered_roles"]
)

print(
    "Missing Roles:",
    coverage["missing_roles"]
)

print(
    "Required Skills:",
    coverage["required_skills"]
)

print(
    "Covered Skills:",
    coverage["covered_skills"]
)

print(
    "Missing Skills:",
    coverage["missing_skills"]
)
print(
    "Skill Owners:",
    coverage["skill_owners"]
)



print("=======================================\n")