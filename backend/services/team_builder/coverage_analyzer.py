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

    Matching strategy:

    1. Exact normalized skill matching
    2. Expanded skill matching
    3. Semantic similarity fallback
    """

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

      

        covered_skills_normalized = set()

        for skill in covered_skills:

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

                    covered_skills_normalized.add(
                        normalized_skill
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

            skill_match_details[
                required_skill
            ] = []

            requirement_covered = False

           

            for required_part in normalized_required_parts:

               

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

                    requirement_covered = True

                    continue

                

                best_match = None
                best_similarity = 0.0

                for candidate_skill in covered_skills:

                    if not candidate_skill:
                        continue

                    similarity = skill_similarity(
                        required_part,
                        candidate_skill
                    )

                    if similarity > best_similarity:

                        best_similarity = similarity

                        best_match = candidate_skill

              

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
                            round(
                                best_similarity,
                                2
                            ),

                        "match_type":
                            "semantic"

                    })

                    requirement_covered = True

                else:

                    skill_match_details[
                        required_skill
                    ].append({

                        "required_skill":
                            required_part,

                        "matched_skill":
                            best_match,

                        "similarity":
                            round(
                                best_similarity,
                                2
                            ),

                        "match_type":
                            "not_covered"

                    })

           

            if not requirement_covered:

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

               

                normalized_student_skills = set()

                for skill in student_skills:

                    if not skill:
                        continue

                    expanded_student_skills = expand_skill(
                        skill
                    )

                    for expanded_skill in expanded_student_skills:

                        normalized_skill = normalize_skill(
                            expanded_skill
                        )

                        if normalized_skill:

                            normalized_student_skills.add(
                                normalized_skill
                            )

                # ----------------------------------
                # Check requirement against member
                # ----------------------------------

                member_can_cover = False

                member_best_similarity = 0.0

                matched_skill = None

                for required_part in normalized_required_parts:

                    # Exact match

                    if (
                        required_part
                        in normalized_student_skills
                    ):

                        member_can_cover = True

                        member_best_similarity = 1.0

                        matched_skill = required_part

                        break

                    # Semantic match

                    best_part_similarity = 0.0
                    best_part_match = None

                    for student_skill in student_skills:

                        if not student_skill:
                            continue

                        similarity = skill_similarity(
                            required_part,
                            student_skill
                        )

                        if (
                            similarity
                            > best_part_similarity
                        ):

                            best_part_similarity = similarity

                            best_part_match = student_skill

                    if (
                        best_part_similarity
                        >= SKILL_SIMILARITY_THRESHOLD
                    ):

                        member_can_cover = True

                        member_best_similarity = (
                            best_part_similarity
                        )

                        matched_skill = best_part_match

                        break

               

                if member_can_cover:

                    skill_owners[
                        required_skill
                    ].append({

                        "student":
                            student_name,

                        "matched_skill":
                            matched_skill,

                        "similarity":
                            round(
                                member_best_similarity,
                                2
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