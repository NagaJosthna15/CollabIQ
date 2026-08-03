from services.matching.skill_matcher import (
    skill_match
)

def rank_candidates(
    project_requirements,
    candidates
):
    ranked_candidates = []

    for candidate in candidates:

        skill_score = skill_match(
    project_requirements.get(
        "required_skills",
        []
    ),
    candidate
)
        domain_score = calculate_domain_score(
        project_requirements,
        candidate
        )
        project_score = calculate_project_score(
        candidate
        )
        career_score = calculate_career_score(
        candidate
        )
        cgpa_score = calculate_cgpa_score(
        candidate
        )
        final_score = calculate_final_score(
            skill_score,
            domain_score,
            project_score,
            career_score,
            cgpa_score
)

        ranked_candidates.append(
    {
        "profile": candidate,
        "scores": {
            "skill": skill_score,
            "domain": domain_score,
            "project": project_score,

            "career": career_score,

            "cgpa": cgpa_score,

            "final": final_score

        }
    }
)
        ranked_candidates.sort(
            key=lambda x:
            x["scores"]["final"],
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
def calculate_project_score(candidate):

    projects = candidate.get(
        "projects_analyzed",
        0
    )

    complexity = candidate.get(
        "average_complexity",
        0
    )

    impact = candidate.get(
        "average_industry_impact",
        0
    )

    future = candidate.get(
        "average_future_scope",
        0
    )

    project_score = min(
        projects * 10,
        100
    )

    final_project_score = (
        project_score * 0.30
        + complexity * 0.25
        + impact * 0.25
        + future * 0.20
    )

    return round(
        final_project_score,
        2
    )
def calculate_cgpa_score(candidate):

    cgpa = candidate.get(
        "cgpa",
        0
    )

    cgpa_score = (
        cgpa / 10
    ) * 100

    return round(
        cgpa_score,
        2
    )
RATING_SCORE = {

    "Exceptional": 100,

    "Excellent": 90,

    "Very Good": 80,

    "Good": 70,

    "Average": 60

}
def calculate_career_score(candidate):

    assessment = candidate.get(
        "career_assessment",
        {}
    )

    rating = assessment.get(
        "overall_rating",
        "Average"
    )

    return RATING_SCORE.get(
        rating,
        60
    )
def calculate_final_score(
    skill_score,
    domain_score,
    project_score,
    career_score,
    cgpa_score
):
    final_score = (

    skill_score * 0.40

    + domain_score * 0.20

    + project_score * 0.20

    + career_score * 0.10

    + cgpa_score * 0.10

)
    return round(
    final_score,
    2
)