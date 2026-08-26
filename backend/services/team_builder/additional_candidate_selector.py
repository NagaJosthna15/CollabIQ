from services.matching.semantic_role_matcher import skill_similarity
from services.matching.skill_normalizer import normalize_skill, expand_skill


class AdditionalCandidateSelector:

    def select_candidates(
        self,
        project_requirements,
        student_profiles,
        selected_team,
        ranked_candidates,
        number_needed=4
    ):

        required_skills = project_requirements.get(
            "required_skills",
            []
        )

        preferred_roles = project_requirements.get(
            "preferred_roles",
            []
        )

        selected_students = set()

        for member in selected_team:

            if not isinstance(member, dict):
                continue

            student_name = member.get("student")

            if not student_name:

                candidate = member.get(
                    "candidate",
                    {}
                )

                if isinstance(candidate, dict):

                    profile = candidate.get(
                        "profile",
                        {}
                    )

                    if isinstance(profile, dict):

                        student_name = profile.get(
                            "student"
                        )

            if not student_name:

                profile = member.get(
                    "profile",
                    {}
                )

                if isinstance(profile, dict):

                    student_name = profile.get(
                        "student"
                    )

            if student_name:

                selected_students.add(
                    student_name
                )

        available_students = {}

        for student in student_profiles:

            if not isinstance(student, dict):
                continue

            student_name = student.get(
                "student"
            )

            if not student_name:

                student_name = student.get(
                    "name"
                )

            if not student_name:
                continue

            if student_name in selected_students:
                continue

            available_students[
                student_name
            ] = student

        candidate_map = {}

        for candidate in ranked_candidates:

            if not isinstance(candidate, dict):
                continue

            profile = candidate.get(
                "profile",
                {}
            )

            student_name = None

            if isinstance(profile, dict):

                student_name = profile.get(
                    "student"
                )

            if not student_name:

                student_name = candidate.get(
                    "student"
                )

            if not student_name:
                continue

            if student_name in selected_students:
                continue

            candidate_map[
                student_name
            ] = candidate

        recommendations = []
        selection_rounds = []

        remaining_skills = list(
            required_skills or []
        )

        remaining_roles = list(
            preferred_roles or []
        )

        while (
            len(recommendations) < number_needed
        ):

            round_candidates = []

            for student_name, student in available_students.items():

                if student_name in selected_students:
                    continue

                student_skills = []

                skills = student.get(
                    "skills",
                    []
                )

                resume_skills = student.get(
                    "resume_skills",
                    []
                )

                if isinstance(skills, list):

                    student_skills.extend(
                        skills
                    )

                if isinstance(resume_skills, list):

                    student_skills.extend(
                        resume_skills
                    )

                best_skill_similarity = 0.0
                best_matched_skill = None
                best_missing_skill = None

                for required_skill in remaining_skills:

                    required_parts = expand_skill(
                        required_skill
                    )

                    for required_part in required_parts:

                        normalized_required_skill = (
                            normalize_skill(
                                required_part
                            )
                        )

                        for student_skill in student_skills:

                            similarity = skill_similarity(
                                normalized_required_skill,
                                student_skill
                            )

                            if similarity > best_skill_similarity:

                                best_skill_similarity = similarity

                                best_matched_skill = student_skill

                                best_missing_skill = required_skill

                ranked_candidate = candidate_map.get(
                    student_name,
                    {}
                )

                candidate_role = ranked_candidate.get(
                    "recommended_role",
                    ""
                )

                if not candidate_role:

                    candidate_role = student.get(
                        "recommended_role",
                        ""
                    )

                if not candidate_role:

                    candidate_role = student.get(
                        "primary_role",
                        ""
                    )

                best_role_similarity = 0.0
                best_matched_role = None

                if candidate_role:

                    for required_role in remaining_roles:

                        similarity = skill_similarity(
                            required_role,
                            candidate_role
                        )

                        if similarity > best_role_similarity:

                            best_role_similarity = similarity

                            best_matched_role = required_role

                ranking_score = ranked_candidate.get(
                    "final_score",
                    ranked_candidate.get(
                        "ranking_score",
                        ranked_candidate.get(
                            "score",
                            0
                        )
                    )
                )

                try:

                    ranking_score = float(
                        ranking_score
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    ranking_score = 0.0

                skill_score = (
                    best_skill_similarity * 50
                )

                role_score = (
                    best_role_similarity * 30
                )

                ranking_component = (
                    ranking_score * 0.20
                )

                overall_score = (
                    skill_score
                    + role_score
                    + ranking_component
                )

                round_candidates.append({

                    "candidate":
                        ranked_candidate,

                    "student":
                        student_name,

                    "score":
                        round(
                            overall_score,
                            2
                        ),

                    "matched_skill":
                        best_matched_skill,

                    "matched_missing_skill":
                        best_missing_skill,

                    "skill_similarity":
                        round(
                            best_skill_similarity,
                            2
                        ),

                    "matched_role":
                        best_matched_role,

                    "role_similarity":
                        round(
                            best_role_similarity,
                            2
                        ),

                    "ranking_score":
                        round(
                            ranking_score,
                            2
                        ),

                    "recommended_role":
                        candidate_role

                })
              
            if not round_candidates:
                break

            round_candidates.sort(
                key=lambda candidate: (
                    candidate["score"],
                    candidate["skill_similarity"],
                    candidate["role_similarity"],
                    candidate["ranking_score"]
                ),
                reverse=True
            )

            minimum_score = 10.0
            round_candidates = [
                candidate
                for candidate in round_candidates
                if candidate["score"] >= minimum_score
            ]
            if not round_candidates:
                break


            best_candidate = round_candidates[0]

            recommendations.append(
                best_candidate
            )

            selection_rounds.append({

                "round":
                    len(recommendations),

                "student":
                    best_candidate[
                        "student"
                    ],

                "score":
                    best_candidate[
                        "score"
                    ],

                "matched_skill":
                    best_candidate[
                        "matched_skill"
                    ],

                "skill_similarity":
                    best_candidate[
                        "skill_similarity"
                    ],

                "matched_role":
                    best_candidate[
                        "matched_role"
                    ],

                "role_similarity":
                    best_candidate[
                        "role_similarity"
                    ]

            })

            selected_students.add(
                best_candidate[
                    "student"
                ]
            )

            matched_missing_skill = best_candidate.get(
                "matched_missing_skill"
            )

            if (
                matched_missing_skill
                and matched_missing_skill
                in remaining_skills
                and best_candidate[
                    "skill_similarity"
                ] >= 0.30
            ):

                remaining_skills.remove(
                    matched_missing_skill
                )

            matched_role = best_candidate.get(
                "matched_role"
            )

            if (
                matched_role
                and matched_role
                in remaining_roles
                and best_candidate[
                    "role_similarity"
                ] >= 0.30
            ):

                remaining_roles.remove(
                    matched_role
                )

        recommended_members = len(
            recommendations
        )

        remaining_members_needed = max(
            0,
            number_needed - recommended_members
        )

        if recommended_members == number_needed:

            status = "full_candidate_coverage"

        elif recommended_members > 0:

            status = "partial_candidate_coverage"

        else:

            status = "no_suitable_candidates"

        return {

            "number_requested":
                number_needed,

            "recommended_candidates":
                recommendations,

            "selection_rounds":
                selection_rounds,

            "remaining_skills":
                remaining_skills,

            "remaining_roles":
                remaining_roles,

            "recommended_members":
                recommended_members,

            "remaining_members_needed":
                remaining_members_needed,

            "status":
                status
        }