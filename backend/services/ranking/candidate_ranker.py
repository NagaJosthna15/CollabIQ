def calculate_skill_score(
    project_requirements,
    candidate
):
    required_skills = project_requirements.get(
        "required_skills",
        []
    )

    skills = candidate.get(
        "skills",
        []
    )

    resume_skills = candidate.get(
        "resume_skills",
        []
    )

    student_skills = skills + resume_skills

    required_skills = [
        skill.lower()
        for skill in required_skills
    ]

    student_skills = [
        skill.lower()
        for skill in student_skills
    ]

    if len(required_skills) == 0:
        return 0

    matches = 0

    for required_skill in required_skills:

        for student_skill in student_skills:

            if (
                required_skill in student_skill
                or student_skill in required_skill
            ):
                matches += 1
                break

    skill_score = (
        matches / len(required_skills)
    ) * 100

    return round(skill_score, 2)


def rank_candidates(
    project_requirements,
    candidates
):
    ranked_candidates = []

    return ranked_candidates