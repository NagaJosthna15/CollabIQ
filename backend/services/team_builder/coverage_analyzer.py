from services.matching.skill_normalizer import (
    normalize_skill,
    expand_skill
)

from services.matching.semantic_role_matcher import (
    skill_similarity
)


SKILL_SIMILARITY_THRESHOLD = 0.70


class CoverageAnalyzer:

    """
    Analyzes whether the selected team covers
    the project's required roles and skills.

    Uses:
    1. Exact/normalized skill matching
    2. Semantic skill similarity
    3. Skill ownership detection
    """

    def analyze(
        self,
        project_requirements,
        selected_team
    ):

        # =================================
        # 1. Project requirements
        # =================================

        required_roles = project_requirements.get(
            "preferred_roles",
            []
        )

        required_skills = project_requirements.get(
            "required_skills",
            []
        )

        # =================================
        # 2. Containers
        # =================================

        covered_roles = []

        covered_skills = []

        # =================================
        # 3. Collect team information
        # =================================

        for member in selected_team:

            # ---------------------------------
            # Primary role
            # ---------------------------------

            primary_role = member.get(
                "role"
            )

            if primary_role:

                covered_roles.append(
                    primary_role
                )

            # ---------------------------------
            # Secondary roles
            # ---------------------------------

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

            # ---------------------------------
            # Student profile
            # ---------------------------------

            profile = member[
                "candidate"
            ]["profile"]

            skills = profile.get(
                "skills",
                []
            )

            resume_skills = profile.get(
                "resume_skills",
                []
            )

            covered_skills.extend(
                skills
            )

            covered_skills.extend(
                resume_skills
            )

        # =================================
        # 4. Normalize roles
        # =================================

        covered_roles_normalized = set(
            role.strip().lower()
            for role in covered_roles
        )

        # =================================
        # 5. Normalize team skills
        # =================================

        covered_skills_normalized = set()

        for skill in covered_skills:

            expanded_skills = expand_skill(
                skill
            )

            for expanded_skill in expanded_skills:

                normalized_skill = normalize_skill(
                    expanded_skill
                )

                covered_skills_normalized.add(
                    normalized_skill
                )

        # =================================
        # 6. Find missing roles
        # =================================

        missing_roles = []

        for role in required_roles:

            role_key = role.strip().lower()

            if role_key not in covered_roles_normalized:

                missing_roles.append(
                    role
                )

        # =================================
        # 7. Semantic skill coverage
        # =================================

        missing_skills = []

        skill_match_details = {}

        for required_skill in required_skills:

            # ---------------------------------
            # Expand required skill
            # ---------------------------------

            required_parts = expand_skill(
                required_skill
            )

            required_parts = [
                normalize_skill(
                    skill
                )
                for skill in required_parts
            ]

            skill_match_details[
                required_skill
            ] = []

            overall_skill_covered = True

            # =================================
            # Check every part of skill
            # =================================

            for required_part in required_parts:

                # ---------------------------------
                # Exact match first
                # ---------------------------------

                if (
                    required_part
                    in covered_skills_normalized
                ):

                    skill_match_details[
                        required_skill
                    ].append({

                        "required_skill":
                            required_part,

                        "matched_skill":
                            required_part,

                        "similarity":
                            1.0,

                        "match_type":
                            "exact"

                    })

                    continue

                # ---------------------------------
                # Semantic matching
                # ---------------------------------

                best_match = None

                best_similarity = 0

                for candidate_skill in covered_skills:

                    similarity = skill_similarity(
                        required_part,
                        candidate_skill
                    )

                    if similarity > best_similarity:

                        best_similarity = similarity

                        best_match = candidate_skill

                # ---------------------------------
                # Threshold check
                # ---------------------------------

                if (
                    best_match is not None
                    and best_similarity
                    >= SKILL_SIMILARITY_THRESHOLD
                ):

                    skill_match_details[
                        required_skill
                    ].append({

                        "required_skill":
                            required_part,

                        "matched_skill":
                            best_match,

                        "similarity":
                            best_similarity,

                        "match_type":
                            "semantic"

                    })

                else:

                    overall_skill_covered = False

                    skill_match_details[
                        required_skill
                    ].append({

                        "required_skill":
                            required_part,

                        "matched_skill":
                            best_match,

                        "similarity":
                            best_similarity,

                        "match_type":
                            "not_covered"

                    })

            # ---------------------------------
            # Add to missing skills
            # ---------------------------------

            if not overall_skill_covered:

                missing_skills.append(
                    required_skill
                )

        # =================================
        # 8. Find skill owners
        # =================================

        skill_owners = {}

        for required_skill in required_skills:

            skill_owners[
                required_skill
            ] = []

            required_parts = expand_skill(
                required_skill
            )

            required_parts = [
                normalize_skill(
                    skill
                )
                for skill in required_parts
            ]

            # =================================
            # Check every team member
            # =================================

            for member in selected_team:

                profile = member[
                    "candidate"
                ]["profile"]

                student_name = profile[
                    "student"
                ]

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

                # ---------------------------------
                # Normalize student skills
                # ---------------------------------

                normalized_student_skills = set()

                for skill in student_skills:

                    expanded_student_skills = expand_skill(
                        skill
                    )

                    for expanded_skill in expanded_student_skills:

                        normalized_student_skills.add(
                            normalize_skill(
                                expanded_skill
                            )
                        )

                # ---------------------------------
                # Check every required part
                # ---------------------------------

                member_can_cover = True

                member_best_similarity = 0

                for required_part in required_parts:

                    # ---------------------------------
                    # Exact match
                    # ---------------------------------

                    if (
                        required_part
                        in normalized_student_skills
                    ):

                        part_similarity = 1.0

                    else:

                        # ---------------------------------
                        # Semantic match
                        # ---------------------------------

                        part_similarity = 0

                        for student_skill in student_skills:

                            similarity = skill_similarity(
                                required_part,
                                student_skill
                            )

                            if similarity > part_similarity:

                                part_similarity = similarity

                    if (
                        part_similarity
                        < SKILL_SIMILARITY_THRESHOLD
                    ):

                        member_can_cover = False

                    member_best_similarity = max(
                        member_best_similarity,
                        part_similarity
                    )

                # ---------------------------------
                # Add owner
                # ---------------------------------

                if member_can_cover:

                    skill_owners[
                        required_skill
                    ].append({

                        "student":
                            student_name,

                        "similarity":
                            round(
                                member_best_similarity,
                                2
                            )

                    })

        # =================================
        # 9. Return complete analysis
        # =================================

        return {

            "required_roles":
                required_roles,

            "covered_roles":
                list(
                    covered_roles_normalized
                ),

            "missing_roles":
                missing_roles,

            "required_skills":
                required_skills,

            "covered_skills":
                list(
                    covered_skills_normalized
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