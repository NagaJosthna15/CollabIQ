from services.talent_scorer import calculate_talent_score
from services.ranker import calculate_final_score
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

        best_student = None
        best_score = -1

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

                match_score = 100

                talent_score = calculate_talent_score(
                    student
                )

                final_score = calculate_final_score(
                    match_score,
                    talent_score
                )

                if final_score > best_score:

                    best_score = final_score
                    best_student = student

        if best_student:

            role = ROLE_MAPPING.get(
                skill.lower(),
                "Team Member"
            )

            team.append({
                "name": best_student["name"],
                "role": role,
                "score": best_score
            })

            selected_students.add(
                best_student["name"]
            )

    return team