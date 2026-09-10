import re

from services.matching.semantic_role_matcher import skill_similarity
from services.matching.skill_normalizer import normalize_skill, expand_skill


SKILL_GAP_THRESHOLD = 0.70


class SkillGapResolver:

    def get_selected_student_name(self, member):
        if not isinstance(member, dict):
            return None

        candidate = member.get("candidate", {})

        if isinstance(candidate, dict):
            profile = candidate.get("profile", {})

            if isinstance(profile, dict):
                student_name = profile.get("student")

                if student_name:
                    return student_name

        student_name = member.get("student_name")

        if student_name:
            return student_name

        student_name = member.get("student")

        if student_name:
            return student_name

        return None

    def get_student_skills(self, student):
        if not isinstance(student, dict):
            return []

        skills = []

        for field in [
            "skills",
            "resume_skills",
            "candidate_skills"
        ]:
            value = student.get(field, [])

            if isinstance(value, list):
                skills.extend(value)

        unique_skills = []
        seen = set()

        for skill in skills:
            if not skill:
                continue

            normalized = normalize_skill(str(skill))

            if normalized and normalized not in seen:
                seen.add(normalized)
                unique_skills.append(skill)

        return unique_skills

    def parse_requirement(self, requirement):
        if not requirement:
            return {
                "type": "simple",
                "base": "",
                "alternatives": []
            }

        text = str(requirement).strip()

        match = re.match(
            r"^(.*?)\s*\((.*?)\)\s*$",
            text
        )

        if match:
            base = match.group(1).strip()
            inner = match.group(2).strip()

            alternatives = [
                part.strip()
                for part in re.split(
                    r",|/|\||\bor\b",
                    inner,
                    flags=re.IGNORECASE
                )
                if part.strip()
            ]

            return {
                "type": "base_with_alternatives",
                "base": base,
                "alternatives": alternatives
            }

        if "/" in text:
            alternatives = [
                part.strip()
                for part in text.split("/")
                if part.strip()
            ]

            if len(alternatives) > 1:
                return {
                    "type": "alternatives",
                    "base": "",
                    "alternatives": alternatives
                }

        return {
            "type": "simple",
            "base": text,
            "alternatives": []
        }

    def match_skill(self, required_skill, student_skills):
        normalized_required = normalize_skill(
            str(required_skill)
        )

        if not normalized_required:
            return None

        best_match = None
        best_similarity = 0.0

        for student_skill in student_skills:
            normalized_student = normalize_skill(
                str(student_skill)
            )

            if not normalized_student:
                continue

            if normalized_required == normalized_student:
                similarity = 1.0
            else:
                similarity = skill_similarity(
                    normalized_required,
                    normalized_student
                )

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = student_skill

        if (
            best_match is not None
            and best_similarity >= SKILL_GAP_THRESHOLD
        ):
            return {
                "matched_skill": best_match,
                "similarity": round(best_similarity, 2)
            }

        return None

    def match_any(self, requirements, student_skills):
        best_match = None

        for requirement in requirements:
            expanded = expand_skill(requirement)

            if not expanded:
                expanded = [requirement]

            for skill in expanded:
                result = self.match_skill(
                    skill,
                    student_skills
                )

                if result is None:
                    continue

                if (
                    best_match is None
                    or result["similarity"]
                    > best_match["similarity"]
                ):
                    best_match = result

        return best_match

    def match_requirement(self, requirement, student_skills):
        parsed = self.parse_requirement(requirement)

        if parsed["type"] == "simple":
            return self.match_any(
                [parsed["base"]],
                student_skills
            )

        if parsed["type"] == "alternatives":
            return self.match_any(
                parsed["alternatives"],
                student_skills
            )

        base = parsed["base"]
        alternatives = parsed["alternatives"]

        base_match = self.match_any(
            [base],
            student_skills
        )

        alternative_match = self.match_any(
            alternatives,
            student_skills
        )

        if base_match and alternative_match:
            if (
                alternative_match["similarity"]
                >= base_match["similarity"]
            ):
                return alternative_match

            return base_match

        if alternative_match:
            return alternative_match

        if base_match:
            return base_match

        return None

    def find_candidates(
        self,
        missing_skills,
        all_students,
        selected_team
    ):
        selected_students = set()

        for member in selected_team or []:
            student_name = self.get_selected_student_name(
                member
            )

            if student_name:
                selected_students.add(
                    str(student_name).lower().strip()
                )

        recommendations = []

        for missing_skill in missing_skills or []:
            candidates = []

            for student in all_students or []:
                if not isinstance(student, dict):
                    continue

                student_name = student.get("student")

                if not student_name:
                    continue

                normalized_name = (
                    str(student_name)
                    .lower()
                    .strip()
                )

                if normalized_name in selected_students:
                    continue

                student_skills = self.get_student_skills(
                    student
                )

                if not student_skills:
                    continue

                match = self.match_requirement(
                    missing_skill,
                    student_skills
                )

                if match is None:
                    continue

                candidates.append({
                    "student": student_name,
                    "matched_skill": match["matched_skill"],
                    "similarity": match["similarity"]
                })

            candidates.sort(
                key=lambda candidate: candidate.get(
                    "similarity",
                    0
                ),
                reverse=True
            )

            if candidates:
                best_candidate = candidates[0]
                status = "candidate_available"

                recommendation = (
                    "Consider adding "
                    + str(best_candidate["student"])
                    + " to improve coverage of "
                    + str(missing_skill)
                    + "."
                )

            else:
                best_candidate = None
                status = "genuine_skill_gap"

                if "nlp" in str(missing_skill).lower():
                    recommendation = (
                        "No suitable candidate with "
                        "sufficient similarity was found. "
                        "Consider upskilling an existing "
                        "team member or recruiting an "
                        "NLP-skilled candidate."
                    )
                else:
                    recommendation = (
                        "No suitable candidate with "
                        "sufficient similarity was found. "
                        "Consider upskilling an existing "
                        "team member or recruiting a "
                        "candidate with this skill."
                    )

            recommendations.append({
                "missing_skill": missing_skill,
                "status": status,
                "best_candidate": best_candidate,
                "candidates": candidates,
                "recommendation": recommendation,
                "is_genuine_gap": not bool(candidates)
            })

        return recommendations