from services.recruiter_agent import RecruiterAgent

from services.team_builder.coverage_analyzer import (
    CoverageAnalyzer
)


# -----------------------------------------
# Create Recruiter Agent
# -----------------------------------------

agent = RecruiterAgent()


# -----------------------------------------
# Recruit the team
# -----------------------------------------

result = agent.recruit_team(
    "AI Healthcare Assistant",
    """
    Build an AI healthcare platform
    using Python, React,
    Machine Learning,
    MongoDB and NLP.
    """
)


# -----------------------------------------
# Get project requirements
# -----------------------------------------

project_requirements = result[
    "project_requirements"
]


# -----------------------------------------
# Get final team
# -----------------------------------------

selected_team = result[
    "final_team"
]


# -----------------------------------------
# Create Coverage Analyzer
# -----------------------------------------

analyzer = CoverageAnalyzer()


# -----------------------------------------
# Analyze coverage
# -----------------------------------------

coverage = analyzer.analyze(
    project_requirements,
    selected_team
)


# -----------------------------------------
# Print result
# -----------------------------------------

print(
    "\n========== COVERAGE ANALYSIS ==========\n"
)

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

print(
    "Skill Match Details:",
    coverage["skill_match_details"]
)

print(
    "=======================================\n"
)