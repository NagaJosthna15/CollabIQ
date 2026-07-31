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

    for candidate in candidates:

        skill_score = calculate_skill_score(
            project_requirements,
            candidate
        )
        domain_score = calculate_domain_score(
        project_requirements,
        candidate
        )

        ranked_candidates.append(
    {
        "profile": candidate,
        "scores": {
            "skill": skill_score,
            "domain": domain_score
        }
    }
)
        ranked_candidates.sort(
        key=lambda x: x["scores"]["skill"],
        reverse=True
    )

    return ranked_candidates
def calculate_domain_score(
    project_requirements,
    candidate
):
    project_domains = project_requirements.get(
        "project_domains",
        []
    )

    strong_domains = candidate.get(
        "strong_domains",
        []
    )

    project_domains = [
        domain.lower()
        for domain in project_domains
    ]

    strong_domains = [
        domain.lower()
        for domain in strong_domains
    ]

    if len(project_domains) == 0:
        return 0

    matches = 0

    for project_domain in project_domains:

        for strong_domain in strong_domains:

            if (
                project_domain in strong_domain
                or strong_domain in project_domain
            ):
                matches += 1
                break

    domain_score = (
        matches / len(project_domains)
    ) * 100

    return round(domain_score, 2)

        

   