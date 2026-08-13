from services.student_service import (
    get_all_students
)

from services.team_builder.team_balance_analyzer import (
    TeamBalanceAnalyzer
)

students = get_all_students()



project_requirements = {

    "estimated_team_size": 6
}


selected_team = [

    {
        "role":
            "Senior Technical Architect",

        "candidate": {

            "profile": {

                "student":
                    "Jyoshna"

            }
        },

        "secondary_roles": [

            {
                "role":
                    "Data Scientist"
            },

            {
                "role":
                    "Healthcare Domain Expert"
            }
        ]
    },

    {
        "role":
            "AI/ML Engineer",

        "candidate": {

            "profile": {

                "student":
                    "Ananya Singh"

            }
        },

        "secondary_roles": [

            {
                "role":
                    "Full Stack Developer"
            },

            {
                "role":
                    "DevOps Engineer"
            }
        ]
    }
]




analyzer = TeamBalanceAnalyzer()




result = analyzer.analyze(
    project_requirements,
    selected_team,
    students
)



print(
    "\n========== TEAM BALANCE ANALYSIS ==========\n"
)

print(
    "Estimated Team Size:",
    result["estimated_team_size"]
)

print(
    "Actual Team Size:",
    result["actual_team_size"]
)

print(
    "Available Candidates:",
    result["available_candidate_count"]
)

print(
    "Maximum Feasible Team Size:",
    result["maximum_feasible_team_size"]
)

print(
    "Members Needed:",
    result["members_needed"]
)

print(
    "Additional Members Available:",
    result["additional_members_available"]
)
print(
    "Size Status:",
    result["size_status"]
)

print(
    "Total Responsibilities:",
    result["total_responsibilities"]
)

print(
    "\nMember Workload:"
)

for member in result["member_workload"]:

    print(
        "\nStudent:",
        member["student"]
    )

    print(
        "Primary Role:",
        member["primary_role"]
    )

    print(
        "Secondary Roles:",
        member["secondary_roles"]
    )

    print(
        "Total Responsibilities:",
        member["total_responsibilities"]
    )

print(
    "\nOverloaded Members:",
    result["overloaded_members"]
)

print(
    "Workload Status:",
    result["workload_status"]
)

print(
    "\nRecommendations:"
)

for recommendation in result[
    "recommendations"
]:

    print(
        "-",
        recommendation
    )

print(
    "\n===========================================\n"
)