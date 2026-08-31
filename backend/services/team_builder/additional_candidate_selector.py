from services.matching.semantic_role_matcher import skill_similarity
from services.matching.skill_normalizer import normalize_skill, expand_skill


def infer_role_from_skills(skills):
    text = " ".join(
        str(skill).lower()
        for skill in (skills or [])
    )

    if any(x in text for x in [
        "tensorflow",
        "pytorch",
        "machine learning",
        "deep learning",
        "nlp",
        "scikit-learn",
        "scikit learn",
        "hugging face",
        "transformers"
    ]):
        return "Machine Learning / NLP Engineer"

    if any(x in text for x in [
        "react",
        "next.js",
        "nextjs",
        "typescript",
        "javascript",
        "html",
        "css"
    ]):
        return "Frontend Engineer"

    if any(x in text for x in [
        "fastapi",
        "flask",
        "django",
        "rest api",
        "node.js",
        "nodejs",
        "express",
        "spring boot",
        "java"
    ]):
        return "Backend Engineer"

    if any(x in text for x in [
        "docker",
        "kubernetes",
        "jenkins",
        "github actions",
        "gitlab ci",
        "aws",
        "azure",
        "gcp"
    ]):
        return "DevOps / Cloud Engineer"

    if any(x in text for x in [
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "etl",
        "data analysis",
        "power bi",
        "excel"
    ]):
        return "Data Engineer"

    return "Software Engineer"


class AdditionalCandidateSelector:

    def __init__(self, semantic_matcher=None):
        self.semantic_matcher = semantic_matcher

    def normalize_skills(self, skills):
        result = []

        for skill in skills or []:
            normalized = normalize_skill(str(skill))

            if not normalized:
                continue

            if normalized not in result:
                result.append(normalized)

            for expanded in expand_skill(normalized) or []:
                if expanded and expanded not in result:
                    result.append(expanded)

        return result

    def extract_requirements(self, project_requirements):
        if not isinstance(project_requirements, dict):
            return [], []

        skills = (
            project_requirements.get("missing_skills")
            or project_requirements.get("skills")
            or project_requirements.get("required_skills")
            or []
        )

        roles = (
            project_requirements.get("missing_roles")
            or project_requirements.get("roles")
            or project_requirements.get("preferred_roles")
            or project_requirements.get("required_roles")
            or []
        )

        return list(skills), list(roles)

    def get_student_name(self, student):
        return str(
            student.get("name")
            or student.get("student")
            or student.get("student_name")
            or student.get("full_name")
            or ""
        ).strip()

    def get_student_skills(self, student):
        skills = (
            student.get("skills")
            or student.get("resume_skills")
            or student.get("technical_skills")
            or []
        )

        if isinstance(skills, str):
            skills = [
                x.strip()
                for x in skills.split(",")
                if x.strip()
            ]

        return skills

    def get_student_role(self, student, skills=None):
        role = (
            student.get("recommended_role")
            or student.get("role")
            or student.get("recommendedRole")
            or ""
        )

        if role:
            return str(role).strip()

        if skills is None:
            skills = self.get_student_skills(student)

        return infer_role_from_skills(skills)

    def get_best_skill_match(
        self,
        candidate_skills,
        required_skills
    ):
        if not candidate_skills or not required_skills:
            return None, 0.0

        candidate_skills = self.normalize_skills(
            candidate_skills
        )

        best_skill = None
        best_score = 0.0

        for candidate_skill in candidate_skills:
            for required_skill in required_skills:

                required_normalized = normalize_skill(
                    str(required_skill)
                )

                if not required_normalized:
                    continue

                if candidate_skill == required_normalized:
                    score = 1.0
                else:
                    try:
                        score = float(
                            skill_similarity(
                                candidate_skill,
                                required_normalized
                            )
                        )
                    except Exception:
                        score = 0.0

                if score > best_score:
                    best_score = score
                    best_skill = required_skill

        return best_skill, round(best_score, 2)

    def get_best_role_match(
        self,
        candidate_role,
        required_roles
    ):
        if not candidate_role or not required_roles:
            return None, 0.0

        candidate = str(candidate_role).lower().strip()

        best_role = None
        best_score = 0.0

        for required_role in required_roles:

            required = str(required_role).lower().strip()

            if candidate == required:
                score = 1.0

            elif candidate in required or required in candidate:
                score = 0.9

            else:
                candidate_words = set(
                    x for x in
                    candidate.replace("/", " ")
                    .replace("-", " ")
                    .split()
                    if len(x) > 2
                )

                required_words = set(
                    x for x in
                    required.replace("/", " ")
                    .replace("-", " ")
                    .split()
                    if len(x) > 2
                )

                common = candidate_words & required_words

                if common:
                    score = len(common) / max(
                        len(candidate_words),
                        len(required_words)
                    )
                else:
                    score = 0.0

            if self.semantic_matcher is not None:
                try:
                    semantic_score = self.semantic_matcher.similarity(
                        candidate_role,
                        required_role
                    )

                    if semantic_score is not None:
                        score = max(
                            score,
                            float(semantic_score)
                        )
                except Exception:
                    pass

            if score > best_score:
                best_score = score
                best_role = required_role

        return best_role, round(best_score, 2)

    def calculate_score(
        self,
        skill_score,
        role_score
    ):
        return round(
            (float(skill_score) * 70)
            +
            (float(role_score) * 30),
            2
        )

    def select_candidates(
        self,
        project_requirements,
        current_team,
        all_students,
        number_needed
    ):
        missing_skills, missing_roles = (
            self.extract_requirements(
                project_requirements
            )
        )

        current_team_names = set()

        for student in current_team or []:
            name = self.get_student_name(student)

            if name:
                current_team_names.add(
                    name.lower()
                )

        candidate_pool = []

        for student in all_students or []:

            name = self.get_student_name(student)

            if not name:
                continue

            if name.lower() in current_team_names:
                continue

            skills = self.get_student_skills(student)

            role = self.get_student_role(
                student,
                skills
            )

            matched_skill, skill_score = (
                self.get_best_skill_match(
                    skills,
                    missing_skills
                )
            )

            matched_role, role_score = (
                self.get_best_role_match(
                    role,
                    missing_roles
                )
            )

            score = self.calculate_score(
                skill_score,
                role_score
            )

            candidate_pool.append({
                "student": name,
                "student_name": name,
                "profile": student,
                "candidate_skills": skills,
                "recommended_role": role,
                "matched_skill": matched_skill,
                "skill_similarity": skill_score,
                "matched_role": matched_role,
                "role_similarity": role_score,
                "overall_score": score,
                "ranking_score": score
            })

        selected = []
        rounds = []

        remaining_skills = list(missing_skills)
        remaining_roles = list(missing_roles)

        while (
            len(selected) < number_needed
            and candidate_pool
        ):
            best = None
            best_score = -1.0

            for candidate in candidate_pool:

                matched_skill, skill_score = (
                    self.get_best_skill_match(
                        candidate["candidate_skills"],
                        remaining_skills
                    )
                )

                matched_role, role_score = (
                    self.get_best_role_match(
                        candidate["recommended_role"],
                        remaining_roles
                    )
                )

                score = self.calculate_score(
                    skill_score,
                    role_score
                )

                candidate["matched_skill"] = matched_skill
                candidate["skill_similarity"] = skill_score
                candidate["matched_role"] = matched_role
                candidate["role_similarity"] = role_score
                candidate["overall_score"] = score
                candidate["ranking_score"] = score

                if score > best_score:
                    best_score = score
                    best = candidate

            if best is None or best_score <= 0:
                break

            selected.append(best)

            rounds.append({
                "round": len(selected),
                "student_name": best["student_name"],
                "selected_student": best["student_name"],
                "score": best["ranking_score"],
                "overall_score": best["overall_score"],
                "matched_skill": best["matched_skill"],
                "matched_role": best["matched_role"]
            })

            if best["matched_skill"] in remaining_skills:
                remaining_skills.remove(
                    best["matched_skill"]
                )

            if best["matched_role"] in remaining_roles:
                remaining_roles.remove(
                    best["matched_role"]
                )

            candidate_pool.remove(best)

        count = len(selected)

        if count == 0:
            status = "no_suitable_candidates"
        elif count == number_needed:
            status = "full_candidate_coverage"
        else:
            status = "partial_candidate_coverage"

        return {
            "recommended_candidates": selected,
            "recommendations": selected,
            "selection_rounds": rounds,

            "missing_skills": missing_skills,
            "missing_roles": missing_roles,

            "remaining_skills": remaining_skills,
            "remaining_roles": remaining_roles,

            "number_requested": number_needed,

            "recommended_members": count,
            "number_selected": count,

            "remaining_members_needed": max(
                number_needed - count,
                0
            ),

            "remaining_needed": max(
                number_needed - count,
                0
            ),

            "status": status
        }