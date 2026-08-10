from services.matching.skill_normalizer import (
    normalize_skill,
    expand_skill
)


class CoverageAnalyzer:

    """
    Analyzes whether the selected team
    covers the project's required roles
    and skills.

    It also identifies which team members
    can provide each required skill.
    """

    def analyze(
        self,
        project_requirements,
        selected_team
    ):

        # --------------------------------
        # 1. Project requirements
        # --------------------------------

        required_roles = project_requirements.get(
            "preferred_roles",
            []
        )

        required_skills = project_requirements.get(
            "required_skills",
            []
        )

        # --------------------------------
        # 2. Containers
        # --------------------------------

        covered_roles = []

        covered_skills = []

        # --------------------------------
        # 3. Analyze selected team
        # --------------------------------

        for member in selected_team:

            # Primary role
            primary_role = member.get(
                "role"
            )

            if primary_role:

                covered_roles.append(
                    primary_role
                )

            # Secondary roles
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

            # Student profile
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

        # --------------------------------
        # 4. Normalize roles
        # --------------------------------

        covered_roles_normalized = set(
            role.strip().lower()
            for role in covered_roles
        )

        # --------------------------------
        # 5. Normalize team skills
        # --------------------------------

        covered_skills_normalized = set()

        for skill in covered_skills:

            expanded_skills = expand_skill(
                skill
            )

            for expanded_skill in expanded_skills:

                covered_skills_normalized.add(
                    normalize_skill(
                        expanded_skill
                    )
                )

        # --------------------------------
        # 6. Find missing roles
        # --------------------------------

        missing_roles = []

        for role in required_roles:

            role_key = role.strip().lower()

            if role_key not in covered_roles_normalized:

                missing_roles.append(
                    role
                )

        # --------------------------------
        # 7. Find missing skills
        # --------------------------------

        missing_skills = []

        for required_skill in required_skills:

            expanded_required_skills = expand_skill(
                required_skill
            )

            skill_is_covered = True

            for skill in expanded_required_skills:

                normalized_required_skill = normalize_skill(
                    skill
                )

                if (
                    normalized_required_skill
                    not in covered_skills_normalized
                ):

                    skill_is_covered = False

                    break

            if not skill_is_covered:

                missing_skills.append(
                    required_skill
                )

        # --------------------------------
        # 8. Find skill owners
        # --------------------------------

        skill_owners = {}

        for required_skill in required_skills:

            skill_owners[
                required_skill
            ] = []

            required_skill_parts = expand_skill(
                required_skill
            )

            normalized_required_parts = [
                normalize_skill(
                    skill
                )
                for skill in required_skill_parts
            ]

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

                # Student owns the skill
                # if all parts are available

                if all(
                    skill in normalized_student_skills
                    for skill in normalized_required_parts
                ):

                    skill_owners[
                        required_skill
                    ].append(
                        student_name
                    )

        # --------------------------------
        # 9. Return coverage analysis
        # --------------------------------

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
                skill_owners
        }