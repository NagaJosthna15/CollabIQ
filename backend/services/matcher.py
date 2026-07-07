def calculate_match_score(student_skills, required_skills):

    student_skills = set(
        skill.lower()
        for skill in student_skills
    )

    required_skills = set(
        skill.lower()
        for skill in required_skills
    )

    matched = student_skills.intersection(
        required_skills
    )

    score = (
        len(matched) /
        len(required_skills)
    ) * 100

    return round(score, 2)