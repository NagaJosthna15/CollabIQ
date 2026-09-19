from database import students_collection, invitations_collection


ROLE_SKILLS = {
    "backend engineer": {
        "java",
        "spring boot",
        "sql",
        "nodejs",
        "node.js",
        "express",
        "mongodb",
        "postgresql",
        "python",
        "fastapi",
        "django",
        "rest api"
    },
    "frontend engineer": {
        "react",
        "javascript",
        "typescript",
        "html",
        "css",
        "next.js",
        "bootstrap"
    },
    "full stack developer": {
        "react",
        "javascript",
        "typescript",
        "nodejs",
        "node.js",
        "express",
        "mongodb",
        "sql",
        "html",
        "css"
    },
    "ai/ml engineer": {
        "python",
        "machine learning",
        "tensorflow",
        "pytorch",
        "nlp",
        "deep learning",
        "scikit-learn",
        "ai"
    },
    "machine learning engineer": {
        "python",
        "machine learning",
        "tensorflow",
        "pytorch",
        "nlp",
        "deep learning",
        "scikit-learn",
        "ai"
    },
    "devops engineer": {
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "ci/cd",
        "github actions"
    },
    "devops / cloud engineer": {
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "ci/cd",
        "github actions"
    },
    "cloud engineer": {
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes"
    },
    "data analyst": {
        "python",
        "sql",
        "power bi",
        "excel",
        "tableau",
        "data analysis"
    }
}


def normalize(value):
    if not value:
        return ""

    return (
        str(value)
        .strip()
        .lower()
        .replace("node.js", "nodejs")
        .replace("next.js", "nextjs")
    )


def find_replacement_candidate(
    project_id,
    role,
    excluded_candidate_ids
):
    excluded_candidate_ids = {
        str(candidate_id)
        for candidate_id in excluded_candidate_ids
    }

    project_invitations = invitations_collection.find({
        "project_id": str(project_id)
    })

    unavailable_candidate_ids = set(
        excluded_candidate_ids
    )

    for invitation in project_invitations:
        candidate_id = invitation.get("candidate_id")

        if candidate_id:
            unavailable_candidate_ids.add(
                str(candidate_id)
            )

    normalized_role = normalize(role)

    role_skills = ROLE_SKILLS.get(
        normalized_role,
        set()
    )

    if not role_skills:
        role_skills = {
            word
            for word in normalized_role.replace(
                "/",
                " "
            ).replace(
                "-",
                " "
            ).split()
            if len(word) > 2
        }

    candidates = []

    for student in students_collection.find({}):
        candidate_id = str(
            student.get("_id", "")
        )

        if candidate_id in unavailable_candidate_ids:
            continue

        candidate_name = (
            student.get("student")
            or student.get("name")
        )

        candidate_email = student.get("email")

        if not candidate_name or not candidate_email:
            continue

        skills = student.get("skills", [])
        resume_skills = student.get(
            "resume_skills",
            []
        )

        all_skills = {
            normalize(skill)
            for skill in (
                skills + resume_skills
            )
            if skill
        }

        recommended_role = normalize(
            student.get(
                "recommended_role",
                ""
            )
        )

        skill_matches = (
            all_skills & role_skills
        )

        role_match = (
            normalized_role == recommended_role
            or normalized_role in recommended_role
            or recommended_role in normalized_role
        )

        score = (
            len(skill_matches) * 10
        )

        if role_match:
            score += 20

        if score > 0:
            candidates.append({
                "student": student,
                "score": score
            })

    if not candidates:
        return None

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return candidates[0]["student"]