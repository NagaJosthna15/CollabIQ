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

        for skill in skills:

            if not skill:
                continue

            expanded_skills = expand_skill(
                skill
            )

            for expanded_skill in expanded_skills:

                normalized_skill = normalize_skill(
                    expanded_skill
                )

                if normalized_skill:

                    normalized_skills.add(
                        normalized_skill
                    )

        return normalized_skills


    def _find_best_match(
        self,
        required_parts,
        available_skills
    ):

        best_match = None
        best_similarity = 0.0

        for required_part in required_parts:

            normalized_required_part = normalize_skill(
                required_part
            )

            if (
                normalized_required_part
                in available_skills
            ):

                return {
                    "covered": True,
                    "required_part": normalized_required_part,
                    "matched_skill": normalized_required_part,
                    "similarity": 1.0,
                    "match_type": "exact"
                }

            for available_skill in available_skills:

                similarity = skill_similarity(
                    normalized_required_part,
                    available_skill
                )

                if similarity > best_similarity:

                    best_similarity = similarity

                    best_match = available_skill

        if (
            best_match is not None
            and best_similarity
            >= SKILL_SIMILARITY_THRESHOLD
        ):

            return {
                "covered": True,
                "required_part": None,
                "matched_skill": best_match,
                "similarity": round(
                    best_similarity,
                    2
                ),
                "match_type": "semantic"
            }

        return {
            "covered": False,
            "required_part": None,
            "matched_skill": best_match,
            "similarity": round(
                best_similarity,
                2
            ),
            "match_type": "not_covered"
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

            required_parts = expand_skill(
                required_skill
            )

            normalized_required_parts = []

            for part in required_parts:

                normalized_part = normalize_skill(
                    part
                )

                if normalized_part:

                    normalized_required_parts.append(
                        normalized_part
                    )

            normalized_required_parts = list(
                dict.fromkeys(
                    normalized_required_parts
                )
            )

            match_result = self._find_best_match(
                normalized_required_parts,
                covered_skills_normalized
            )

            skill_match_details[
                required_skill
            ] = [{

                "required_skill":
                    match_result.get(
                        "required_part"
                    ),

                "matched_skill":
                    match_result.get(
                        "matched_skill"
                    ),

                "similarity":
                    match_result.get(
                        "similarity"
                    ),

                "match_type":
                    match_result.get(
                        "match_type"
                    )

            }]

            if not match_result.get(
                "covered"
            ):

                missing_skills.append(
                    required_skill
                )

        skill_owners = {}

        for required_skill in required_skills:

            skill_owners[
                required_skill
            ] = []

            required_parts = expand_skill(
                required_skill
            )

            normalized_required_parts = []

            for part in required_parts:

                normalized_part = normalize_skill(
                    part
                )

                if normalized_part:

                    normalized_required_parts.append(
                        normalized_part
                    )

            normalized_required_parts = list(
                dict.fromkeys(
                    normalized_required_parts
                )
            )

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

                match_result = self._find_best_match(
                    normalized_required_parts,
                    normalized_student_skills
                )

                if match_result.get(
                    "covered"
                ):

                    skill_owners[
                        required_skill
                    ].append({

                        "student":
                            student_name,

                        "matched_skill":
                            match_result.get(
                                "matched_skill"
                            ),

                        "similarity":
                            match_result.get(
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