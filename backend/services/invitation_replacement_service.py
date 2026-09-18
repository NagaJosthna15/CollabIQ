from database import students_collection, invitations_collection


def find_replacement_candidate(
    project_id,
    role,
    excluded_candidate_ids
):
    excluded_candidate_ids = {
        str(candidate_id)
        for candidate_id in excluded_candidate_ids
    }

    invited_candidates = invitations_collection.find({
        "project_id": str(project_id)
    })

    unavailable_candidate_ids = set(excluded_candidate_ids)

    for invitation in invited_candidates:
        status = invitation.get("status")

        if status in {"invited", "accepted", "rejected"}:
            candidate_id = invitation.get("candidate_id")

            if candidate_id:
                unavailable_candidate_ids.add(
                    str(candidate_id)
                )

    students = students_collection.find({})

    candidates = []

    for student in students:

        candidate_id = str(student.get("_id", ""))

        if candidate_id in unavailable_candidate_ids:
            continue

        student_name = (
            student.get("student")
            or student.get("name")
        )

        email = student.get("email")

        if not student_name or not email:
            continue

        skills = student.get("skills", [])
        resume_skills = student.get("resume_skills", [])

        all_skills = {
            str(skill).strip().lower()
            for skill in skills + resume_skills
            if skill
        }

        role_text = str(
            student.get("recommended_role", "")
        ).strip().lower()

        role_words = {
            word.strip()
            for word in role.lower().replace("/", " ").replace("-", " ").split()
            if len(word.strip()) > 2
        }

        skill_score = 0

        for skill in all_skills:
            for word in role_words:
                if word in skill or skill in word:
                    skill_score += 1

        role_score = sum(
            1
            for word in role_words
            if word in role_text
        )

        total_score = skill_score + role_score

        if total_score > 0:
            candidates.append({
                "student": student,
                "score": total_score
            })

    if not candidates:
        return None

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return candidates[0]["student"]