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

from services.llm.llm_career_assessor import (
    generate_career_assessment
)


def build_student_profile(student):

    github_username = student.get(
        "github_username",
        ""
    )

    student_name = student.get(
        "name",
        student.get("student", "")
    )

    email = student.get(
        "email",
        ""
    )

    skills = student.get(
        "skills",
        []
    ) or []

    resume_skills = student.get(
        "resume_skills",
        []
    ) or []

    cgpa = student.get(
        "cgpa",
        0
    )

    profile = {
        "student_id": str(
            student.get("_id", "")
        ),
        "student": student_name,
        "email": email,
        "github_username": github_username,
        "cgpa": cgpa,
        "skills": skills,
        "resume_skills": resume_skills,
        "projects_analyzed": 0,
        "strong_domains": [],
        "average_innovation": 0,
        "average_complexity": 0,
        "average_industry_impact": 0,
        "average_future_scope": 0,
        "recommended_role": "Software Engineer"
    }

    if not github_username:
        return profile

    try:
        repositories = get_github_repositories(
            github_username
        )
    except Exception:
        repositories = []

    project_reports = []

    for repo in repositories:

        repo_name = repo.get(
            "name",
            ""
        )

        if not repo_name:
            continue

        try:
            readme = get_readme(
                github_username,
                repo_name
            )
        except Exception:
            continue

        if not readme:
            continue

        try:
            report = analyze_project(
                readme
            )
        except Exception:
            continue

        if not isinstance(report, dict):
            continue

        project_reports.append({
            "repository": repo_name,
            "analysis": report
        })

    if project_reports:

        domain_count = {}

        total_innovation = 0
        total_complexity = 0
        total_industry_impact = 0
        total_future_scope = 0

        valid_reports = 0

        for project in project_reports:

            analysis = project.get(
                "analysis",
                {}
            )

            try:
                innovation = float(
                    analysis.get(
                        "innovation_score",
                        0
                    )
                )
            except (TypeError, ValueError):
                innovation = 0

            try:
                complexity = float(
                    analysis.get(
                        "complexity_score",
                        0
                    )
                )
            except (TypeError, ValueError):
                complexity = 0

            try:
                industry_impact = float(
                    analysis.get(
                        "industry_impact_score",
                        analysis.get(
                            "industry_impact",
                            0
                        )
                    )
                )
            except (TypeError, ValueError):
                industry_impact = 0

            try:
                future_scope = float(
                    analysis.get(
                        "future_scope_score",
                        analysis.get(
                            "future_scope",
                            0
                        )
                    )
                )
            except (TypeError, ValueError):
                future_scope = 0

            total_innovation += innovation
            total_complexity += complexity
            total_industry_impact += industry_impact
            total_future_scope += future_scope

            valid_reports += 1

            domains = analysis.get(
                "top_domains",
                []
            ) or []

            for domain in domains:

                if not domain:
                    continue

                domain_count[domain] = (
                    domain_count.get(
                        domain,
                        0
                    ) + 1
                )

        profile["projects_analyzed"] = len(
            project_reports
        )

        if valid_reports > 0:

            profile["average_innovation"] = round(
                total_innovation / valid_reports,
                2
            )

            profile["average_complexity"] = round(
                total_complexity / valid_reports,
                2
            )

            profile["average_industry_impact"] = round(
                total_industry_impact / valid_reports,
                2
            )

            profile["average_future_scope"] = round(
                total_future_scope / valid_reports,
                2
            )

        strong_domains = sorted(
            domain_count,
            key=domain_count.get,
            reverse=True
        )[:3]

        profile["strong_domains"] = strong_domains

        recommended_role = "Software Engineer"

        if strong_domains:

            recommended_role = ROLE_MAPPING.get(
                strong_domains[0],
                "Software Engineer"
            )

            if (
                "Artificial Intelligence"
                in strong_domains
                and
                "Web Development"
                in strong_domains
            ):
                recommended_role = (
                    "AI Solutions Engineer"
                )

        profile["recommended_role"] = (
            recommended_role
        )

    else:

        skill_text = " ".join(
            str(skill).lower()
            for skill in (
                skills + resume_skills
            )
        )

        if any(
            keyword in skill_text
            for keyword in [
                "machine learning",
                "tensorflow",
                "pytorch",
                "scikit-learn",
                "nlp",
                "artificial intelligence"
            ]
        ):
            profile["recommended_role"] = (
                "AI/ML Engineer"
            )

        elif any(
            keyword in skill_text
            for keyword in [
                "react",
                "javascript",
                "typescript",
                "html",
                "css",
                "next.js"
            ]
        ) and any(
            keyword in skill_text
            for keyword in [
                "node.js",
                "nodejs",
                "express",
                "mongodb",
                "postgresql"
            ]
        ):
            profile["recommended_role"] = (
                "Full Stack Developer"
            )

        elif any(
            keyword in skill_text
            for keyword in [
                "react",
                "javascript",
                "typescript",
                "html",
                "css",
                "next.js"
            ]
        ):
            profile["recommended_role"] = (
                "Frontend Engineer"
            )

        elif any(
            keyword in skill_text
            for keyword in [
                "python",
                "flask",
                "fastapi",
                "django",
                "rest api"
            ]
        ):
            profile["recommended_role"] = (
                "Backend Engineer"
            )

        elif any(
            keyword in skill_text
            for keyword in [
                "aws",
                "azure",
                "gcp",
                "docker",
                "kubernetes",
                "ci/cd",
                "github actions"
            ]
        ):
            profile["recommended_role"] = (
                "DevOps / Cloud Engineer"
            )

        elif any(
            keyword in skill_text
            for keyword in [
                "sql",
                "mysql",
                "postgresql",
                "power bi",
                "excel",
                "data analysis"
            ]
        ):
            profile["recommended_role"] = (
                "Data Analyst"
            )

        elif any(
            keyword in skill_text
            for keyword in [
                "spring boot",
                "java"
            ]
        ):
            profile["recommended_role"] = (
                "Java Backend Engineer"
            )

    try:
        profile["career_assessment"] = (
            generate_career_assessment(
                profile
            )
        )
    except Exception:
        profile["career_assessment"] = {
            "overall_rating": "Unavailable",
            "reason": (
                "Career assessment could not be generated."
            ),
            "strengths": [],
            "growth_areas": [],
            "career_advice": "",
            "recommended_projects": [],
            "next_learning_path": []
        }

    return profile