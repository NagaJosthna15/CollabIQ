def calculate_talent_score(student):

    skills_count = len(student.get("resume_skills", []))

    projects_completed = student.get("projects_completed", 0)

    cgpa = student.get("cgpa", 0)


    skill_score = skills_count * 3
    project_score = projects_completed * 5
    cgpa_score = cgpa * 2

    total_score = (
        skill_score
        + project_score
        + cgpa_score
    )

    return round(total_score, 2)