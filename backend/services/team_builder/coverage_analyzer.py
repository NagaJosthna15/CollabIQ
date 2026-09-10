import re

from services.matching.skill_normalizer import (
    normalize_skill,
    expand_skill
)

from services.matching.semantic_role_matcher import (
    skill_similarity
)


SKILL_SIMILARITY_THRESHOLD = 0.70


class CoverageAnalyzer:

    def _normalize_skills(self, skills):
        normalized_skills = set()

        for skill in skills or []:
            if not skill:
                continue

            expanded_skills = expand_skill(skill)

            for expanded_skill in expanded_skills:
                normalized_skill = normalize_skill(
                    expanded_skill
                )

                if normalized_skill:
                    normalized_skills.add(
                        normalized_skill
                    )

        return normalized_skills

    def _semantic_match(
        self,
        required_skill,
        available_skills
    ):
        best_match = None
        best_similarity = 0.0

        normalized_required = normalize_skill(
            required_skill
        )

        for available_skill in available_skills:
            normalized_available = normalize_skill(
                available_skill
            )

            if not normalized_available:
                continue

            if normalized_available == normalized_required:
                return {
                    "covered": True,
                    "matched_skill": normalized_available,
                    "similarity": 1.0,
                    "match_type": "exact"
                }

            try:
                similarity = skill_similarity(
                    normalized_required,
                    normalized_available
                )
            except Exception:
                similarity = 0.0

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = normalized_available

        if (
            best_match is not None
            and best_similarity >= SKILL_SIMILARITY_THRESHOLD
        ):
            return {
                "covered": True,
                "matched_skill": best_match,
                "similarity": round(
                    best_similarity,
                    2
                ),
                "match_type": "semantic"
            }

        return {
            "covered": False,
            "matched_skill": best_match,
            "similarity": round(
                best_similarity,
                2
            ),
            "match_type": "not_covered"
        }

    def _parse_requirement(self, requirement):
        text = str(requirement).strip()

        if not text:
            return {
                "base": [],
                "alternatives": [],
                "mode": "simple"
            }

        match = re.match(
            r"^(.*?)\s*\((.*?)\)\s*$",
            text
        )

        if match:
            base_text = match.group(1).strip()
            alternative_text = match.group(2).strip()

            base = []

            if base_text:
                base = [
                    normalize_skill(base_text)
                ]

            alternatives = []

            parts = re.split(
                r"[/|,]",
                alternative_text
            )

            for part in parts:
                normalized_part = normalize_skill(
                    part.strip()
                )

                if normalized_part:
                    alternatives.append(
                        normalized_part
                    )

            return {
                "base": base,
                "alternatives": list(
                    dict.fromkeys(alternatives)
                ),
                "mode": "compound"
            }

        slash_parts = [
            part.strip()
            for part in re.split(
                r"\s*/\s*",
                text
            )
            if part.strip()
        ]

        if len(slash_parts) > 1:
            normalized_parts = [
                normalize_skill(part)
                for part in slash_parts
            ]

            return {
                "base": [],
                "alternatives": list(
                    dict.fromkeys(
                        part
                        for part in normalized_parts
                        if part
                    )
                ),
                "mode": "alternative"
            }

        expanded = expand_skill(text)

        normalized_parts = [
            normalize_skill(part)
            for part in expanded
            if normalize_skill(part)
        ]

        normalized_parts = list(
            dict.fromkeys(normalized_parts)
        )

        if len(normalized_parts) > 1:
            return {
                "base": [],
                "alternatives": normalized_parts,
                "mode": "alternative"
            }

        return {
            "base": normalized_parts,
            "alternatives": [],
            "mode": "simple"
        }

    def _check_requirement(
        self,
        requirement,
        available_skills
    ):
        parsed = self._parse_requirement(
            requirement
        )

        details = []

        for base_skill in parsed["base"]:
            result = self._semantic_match(
                base_skill,
                available_skills
            )

            details.append({
                "required_skill": base_skill,
                "matched_skill": result.get(
                    "matched_skill"
                ),
                "similarity": result.get(
                    "similarity"
                ),
                "match_type": result.get(
                    "match_type"
                )
            })

            if not result.get("covered"):
                return {
                    "covered": False,
                    "details": details,
                    "matched_skill": result.get(
                        "matched_skill"
                    ),
                    "similarity": result.get(
                        "similarity"
                    )
                }

        alternative_match = None

        for alternative in parsed["alternatives"]:
            result = self._semantic_match(
                alternative,
                available_skills
            )

            details.append({
                "required_skill": alternative,
                "matched_skill": result.get(
                    "matched_skill"
                ),
                "similarity": result.get(
                    "similarity"
                ),
                "match_type": result.get(
                    "match_type"
                )
            })

            if result.get("covered"):
                alternative_match = result
                break

        if parsed["alternatives"]:
            if alternative_match:
                return {
                    "covered": True,
                    "details": details,
                    "matched_skill":
                        alternative_match.get(
                            "matched_skill"
                        ),
                    "similarity":
                        alternative_match.get(
                            "similarity"
                        )
                }

            return {
                "covered": False,
                "details": details,
                "matched_skill": None,
                "similarity": 0.0
            }

        if parsed["base"]:
            best_detail = max(
                details,
                key=lambda item:
                item.get("similarity", 0.0)
            )

            return {
                "covered": True,
                "details": details,
                "matched_skill":
                    best_detail.get(
                        "matched_skill"
                    ),
                "similarity":
                    best_detail.get(
                        "similarity"
                    )
            }

        return {
            "covered": False,
            "details": details,
            "matched_skill": None,
            "similarity": 0.0
        }

    def analyze(
        self,
        project_requirements,
        selected_team
    ):
        required_roles = project_requirements.get(
            "preferred_roles",
            []
        )

        required_skills = project_requirements.get(
            "required_skills",
            []
        )

        covered_roles = []
        covered_skills = []

        for member in selected_team:
            primary_role = member.get(
                "role"
            )

            if primary_role:
                covered_roles.append(
                    primary_role
                )

            secondary_roles = member.get(
                "secondary_roles",
                []
            )

            for secondary in secondary_roles:
                secondary_role = secondary.get(
                    "role"
                )

                if secondary_role:
                    covered_roles.append(
                        secondary_role
                    )

            candidate = member.get(
                "candidate",
                {}
            )

            profile = candidate.get(
                "profile",
                {}
            )

            covered_skills.extend(
                profile.get(
                    "skills",
                    []
                )
            )

            covered_skills.extend(
                profile.get(
                    "resume_skills",
                    []
                )
            )

        covered_roles_normalized = set()

        for role in covered_roles:
            if role:
                covered_roles_normalized.add(
                    role.strip().lower()
                )

        covered_skills_normalized = (
            self._normalize_skills(
                covered_skills
            )
        )

        missing_roles = []

        for role in required_roles:
            if not role:
                continue

            role_key = role.strip().lower()

            if role_key not in covered_roles_normalized:
                missing_roles.append(
                    role
                )

        missing_skills = []
        skill_match_details = {}

        for required_skill in required_skills:
            result = self._check_requirement(
                required_skill,
                covered_skills_normalized
            )

            skill_match_details[
                required_skill
            ] = result.get(
                "details",
                []
            )

            if not result.get("covered"):
                missing_skills.append(
                    required_skill
                )

        skill_owners = {}

        for required_skill in required_skills:
            skill_owners[
                required_skill
            ] = []

            for member in selected_team:
                candidate = member.get(
                    "candidate",
                    {}
                )

                profile = candidate.get(
                    "profile",
                    {}
                )

                student_name = profile.get(
                    "student",
                    "Unknown"
                )

                student_skills = []

                student_skills.extend(
                    profile.get(
                        "skills",
                        []
                    )
                )

                student_skills.extend(
                    profile.get(
                        "resume_skills",
                        []
                    )
                )

                normalized_student_skills = (
                    self._normalize_skills(
                        student_skills
                    )
                )

                result = self._check_requirement(
                    required_skill,
                    normalized_student_skills
                )

                if result.get("covered"):
                    skill_owners[
                        required_skill
                    ].append({
                        "student":
                            student_name,
                        "matched_skill":
                            result.get(
                                "matched_skill"
                            ),
                        "similarity":
                            result.get(
                                "similarity"
                            )
                    })

        return {
            "required_roles":
                required_roles,
            "covered_roles":
                sorted(
                    list(
                        covered_roles_normalized
                    )
                ),
            "missing_roles":
                missing_roles,
            "required_skills":
                required_skills,
            "covered_skills":
                sorted(
                    list(
                        covered_skills_normalized
                    )
                ),
            "missing_skills":
                missing_skills,
            "skill_owners":
                skill_owners,
            "skill_match_details":
                skill_match_details,
            "skill_similarity_threshold":
                SKILL_SIMILARITY_THRESHOLD
        }