from services.agents.responsibility_agent import (
    ResponsibilityAgent
)

agent = ResponsibilityAgent()

selected_team = [

    {
        "role": "AI Engineer",

        "candidate": {

            "profile": {

                "student": "Jyoshna",

                "recommended_role":
                "AI Solutions Engineer",

                "skills": [
                    "Python",
                    "Machine Learning",
                    "React"
                ],

                "resume_skills": [
                    "MongoDB",
                    "Docker",
                    "Flask"
                ],

                "strong_domains": [
                    "Artificial Intelligence",
                    "Automation"
                ]
            }
        }
    },

    {
        "role": "Frontend Developer",

        "candidate": {

            "profile": {

                "student":
                "Ananya Singh",

                "recommended_role":
                "Cloud Engineer",

                "skills": [
                    "React",
                    "Node.js",
                    "MongoDB"
                ],

                "resume_skills": [
                    "Docker",
                    "AWS",
                    "JavaScript"
                ],

                "strong_domains": [
                    "Cloud Computing",
                    "Web Development"
                ]
            }
        }
    }

]

response = agent.assign_secondary_role(

    "DevOps Engineer",

    selected_team

)

print(response)