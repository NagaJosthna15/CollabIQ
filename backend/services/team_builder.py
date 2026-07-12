ROLE_MAPPING = {
    "python": "AI Developer",
    "machine learning": "ML Engineer",
    "react": "Frontend Developer",
    "nodejs": "Backend Developer",
    "mongodb": "Database Engineer",
    "sql": "Database Engineer",
    "power bi": "Data Analyst",
    "excel": "Business Analyst"
}

def build_balanced_team(project, students):

    required_skills = project.get(
        "required_skills",
        []
    )

    team = []

    selected_students = set()

    for skill in required_skills:

        for student in students:

            if student["name"] in selected_students:
                continue

            student_skills = [
                s.lower()
                for s in student.get(
                    "resume_skills",
                    []
                )
            ]

            if skill.lower() in student_skills:
                role = ROLE_MAPPING.get(
                      skill.lower(),
                      "Team Member"
                      )
                team.append({
                    "name": student["name"],
                    "role": role
                    })

               
                selected_students.add(
                    student["name"]
                )

                break

    return team