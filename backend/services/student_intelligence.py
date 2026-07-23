ROLE_MAPPING = {
    "Artificial Intelligence": "AI Engineer",
    "Machine Learning": "ML Engineer",
    "Data Analytics": "Data Analyst",
    "Web Development": "Full Stack Developer",
    "Automation": "Automation Engineer",
    "Cloud Computing": "Cloud Engineer",
    "FinTech": "FinTech Developer",
    "Cybersecurity": "Security Engineer"
}
from services.github_analyzer import (
    get_github_repositories,
)

from services.github_readme_fetcher import (
    get_readme
)

from services.project_intelligence import (
    analyze_project
)
from services.llm.llm_career_assessor import generate_career_assessment

def build_student_profile(student):

    github_username = student["github_username"]

    repositories = get_github_repositories(github_username)

    project_reports = []

    for repo in repositories:

        repo_name = repo["name"]

        readme = get_readme(
            github_username,
            repo_name
        )

        if not readme:
            continue

        report = analyze_project(readme)

        project_reports.append({
            "repository": repo_name,
            "analysis": report
        })

    if not project_reports:
        return {
            "student": github_username,
            "projects_analyzed": 0
        }

    domain_count = {}

    total_innovation = 0
    total_complexity = 0
    total_industry_impact = 0
    total_future_scope = 0

    for project in project_reports:

        analysis = project["analysis"]

        total_innovation += analysis["innovation_score"]
        total_complexity += analysis["complexity_score"]
        total_industry_impact += analysis["industry_impact"]
        total_future_scope += analysis["future_scope"]

        for domain in analysis["top_domains"]:

            domain_count[domain] = (
                domain_count.get(domain, 0) + 1
            )

    strong_domains = sorted(
        domain_count,
        key=domain_count.get,
        reverse=True
    )[:3]

    recommended_role = "Software Engineer"

    if strong_domains:

        recommended_role = ROLE_MAPPING.get(
            strong_domains[0],
            "Software Engineer"
        )

        if (
            "Artificial Intelligence" in strong_domains
            and
            "Web Development" in strong_domains
        ):
            recommended_role = (
                "AI Solutions Engineer"
            )

    avg_innovation = round(
        total_innovation / len(project_reports),
        2
    )

    avg_complexity = round(
        total_complexity / len(project_reports),
        2
    )

    avg_industry_impact = round(
        total_industry_impact / len(project_reports),
        2
    )

    avg_future_scope = round(
        total_future_scope / len(project_reports),
        2
    )

    profile = {
    "student_id": str(student.get("_id", "")),
    "student": student["name"],
    "email": student["email"],
    "github_username": github_username,
    "cgpa": student.get("cgpa", 0),
    "skills": student.get("skills", []),
    "resume_skills": student.get("resume_skills", []),

    "projects_analyzed": len(project_reports),

    "strong_domains": strong_domains,

    "average_innovation": avg_innovation,
    "average_complexity": avg_complexity,
    "average_industry_impact": avg_industry_impact,
    "average_future_scope": avg_future_scope,

    "recommended_role": recommended_role
}

    profile["career_assessment"] = (
        generate_career_assessment(profile)
    )

    return profile
