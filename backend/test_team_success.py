from services.team_success import calculate_team_success

team = [
    {
        "role": "AI/ML Engineer",
        "selection_score": 77.7,
        "candidate": {
            "profile": {
                "skills": [
                    "Python",
                    "Machine Learning",
                    "Power BI"
                ],
                "resume_skills": [
                    "machine learning",
                    "sql",
                    "flask",
                    "mongodb",
                    "react"
                ]
            }
        }
    },
    {
        "role": "Backend Engineer",
        "selection_score": 52.6,
        "candidate": {
            "profile": {
                "skills": [
                    "Python",
                    "SQL"
                ],
                "resume_skills": [
                    "python",
                    "sql",
                    "excel"
                ]
            }
        }
    },
    {
        "role": "DevOps / Cloud Engineer",
        "selection_score": 48.55,
        "candidate": {
            "profile": {
                "skills": [
                    "React",
                    "Node.js",
                    "MongoDB"
                ],
                "resume_skills": [
                    "react",
                    "nodejs",
                    "mongodb",
                    "javascript"
                ]
            }
        }
    }
]

result = calculate_team_success(team)

print("TEAM SUCCESS RESULT")
print(result)