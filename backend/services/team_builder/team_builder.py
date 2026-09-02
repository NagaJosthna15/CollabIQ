from services.agents.responsibility_agent import (
    ResponsibilityAgent
)

from services.matching.semantic_role_matcher import (
    role_similarity
)

from services.team_builder.coverage_analyzer import (
    CoverageAnalyzer
)

from services.team_builder.skill_gap_resolver import (
    SkillGapResolver
)

from services.team_builder.additional_candidate_selector import (
    AdditionalCandidateSelector
)

from services.student_service import (
    get_all_students
)


MIN_PRIMARY_SCORE = 40


def assign_primary_roles(
    project_requirements,
    ranked_candidates
):
    preferred_roles = project_requirements.get(
        "preferred_roles",
        []
    )

    selected_team = []
    unassigned_roles = []
    used_students = set()

    for role in preferred_roles:

        print(
            "\nSearching:",
            role
        )

        best_candidate = None
        best_score = 0

        for candidate in ranked_candidates:

            profile = candidate.get(
                "profile",
                {}
            )

            student_name = profile.get(
                "student"
            )

            if not student_name:
                continue

            if student_name in used_students:
                continue

            recommended_role = profile.get(
                "recommended_role",
                ""
            )

            similarity = role_similarity(
                role,
                recommended_role
            )

            skill_score = candidate.get(
                "scores",
                {}
            ).get(
                "skill",
                0
            )

            ranking_score = candidate.get(
                "scores",
                {}
            ).get(
                "final",
                0
            )

            combined_score = (
                (similarity * 40)
                + (skill_score * 0.35)
                + (ranking_score * 0.25)
            )

            print(
                profile.get("student"),
                "| Role:",
                recommended_role,
                "| Similarity:",
                round(similarity, 2),
                "| Skill:",
                skill_score,
                "| Ranking:",
                ranking_score,
                "| Combined:",
                round(combined_score, 2)
            )

            if combined_score > best_score:

                best_score = combined_score
                best_candidate = candidate

        if (
            best_candidate is not None
            and best_score >= MIN_PRIMARY_SCORE
        ):

            student_name = (
                best_candidate["profile"]["student"]
            )

            selected_team.append({
                "role": role,
                "candidate": best_candidate,
                "selection_score": round(
                    best_score,
                    2
                )
            })

            used_students.add(
                student_name
            )

            print(
                "Selected:",
                student_name,
                "| Score:",
                round(best_score, 2)
            )

        else:

            unassigned_roles.append(
                role
            )

            if best_candidate is not None:

                print(
                    "No suitable unused candidate for:",
                    role,
                    "| Best Score:",
                    round(best_score, 2)
                )

            else:

                print(
                    "No unused candidate available for:",
                    role
                )

    return {
        "selected_team": selected_team,
        "unassigned_roles": unassigned_roles
    }


def assign_secondary_roles(
    project_requirements,
    selected_team,
    unassigned_roles
):
    agent = ResponsibilityAgent()

    for role in unassigned_roles:

        print(
            "\nReassigning:",
            role
        )

        result = agent.assign_secondary_role(
            role,
            selected_team
        )

        print(result)

        selected_student = result.get(
            "selected_student"
        )

        confidence = result.get(
            "confidence"
        )

        reason = result.get(
            "reason"
        )

        if not selected_student:
            continue

        for member in selected_team:

            student_name = member[
                "candidate"
            ]["profile"]["student"]

            if student_name == selected_student:

                if "secondary_roles" not in member:
                    member["secondary_roles"] = []

                member["secondary_roles"].append({
                    "role": role,
                    "confidence": confidence,
                    "reason": reason
                })

                break

    return selected_team


def build_team(
    project_requirements,
    ranked_candidates
):

    # ==========================================
    # STEP 1: PRIMARY ROLE ASSIGNMENT
    # ==========================================

    primary_result = assign_primary_roles(
        project_requirements,
        ranked_candidates
    )

    selected_team = primary_result.get(
        "selected_team",
        []
    )

    # ==========================================
    # STEP 2: INITIAL COVERAGE ANALYSIS
    # ==========================================

    coverage_analyzer = CoverageAnalyzer()

    initial_coverage = coverage_analyzer.analyze(
        project_requirements,
        selected_team
    )

    print(
        "\n========== INITIAL COVERAGE =========="
    )

    print(
        "Missing Roles:",
        initial_coverage.get(
            "missing_roles",
            []
        )
    )

    print(
        "Missing Skills:",
        initial_coverage.get(
            "missing_skills",
            []
        )
    )

    print(
        "======================================\n"
    )

    # ==========================================
    # STEP 3: SECONDARY ROLE ASSIGNMENT
    # ==========================================

    missing_roles = initial_coverage.get(
        "missing_roles",
        []
    )

    selected_team = assign_secondary_roles(
        project_requirements,
        selected_team,
        missing_roles
    )

    # ==========================================
    # STEP 4: FINAL COVERAGE ANALYSIS
    # ==========================================

    final_coverage = coverage_analyzer.analyze(
        project_requirements,
        selected_team
    )

    print(
        "\n========== FINAL COVERAGE =========="
    )

    print(
        "Missing Roles:",
        final_coverage.get(
            "missing_roles",
            []
        )
    )

    print(
        "Missing Skills:",
        final_coverage.get(
            "missing_skills",
            []
        )
    )

    print(
        "====================================\n"
    )

    # ==========================================
    # STEP 5: GET ALL STUDENTS
    # ==========================================

    all_students = get_all_students()

    # ==========================================
    # STEP 6: ADDITIONAL CANDIDATE SELECTION
    # ==========================================

    remaining_roles = final_coverage.get(
        "missing_roles",
        []
    )

    remaining_skills = final_coverage.get(
        "missing_skills",
        []
    )

    additional_candidate_result = {
        "recommended_candidates": [],
        "recommendations": [],
        "selection_rounds": [],
        "remaining_skills": remaining_skills,
        "remaining_roles": remaining_roles,
        "number_requested": 0,
        "recommended_members": 0,
        "number_selected": 0,
        "remaining_members_needed": 0,
        "status": "not_required"
    }

    number_requested = len(
        remaining_roles
    )

    if number_requested > 0 or remaining_skills:

        # If roles are already covered but
        # skills are still missing
        if number_requested == 0:

            number_requested = min(
                3,
                len(remaining_skills)
            )

        additional_selector = (
            AdditionalCandidateSelector()
        )

        additional_requirements = {
            "skills": remaining_skills,
            "roles": remaining_roles,

            # Compatibility with existing
            # project requirement structure
            "preferred_roles": remaining_roles
        }

        additional_candidate_result = (
            additional_selector.select_candidates(
                additional_requirements,
                selected_team,
                all_students,
                number_requested
            )
        )

        print(
            "\n========== ADDITIONAL CANDIDATE SELECTION =========="
        )

        print(
            "Members Requested:",
            number_requested
        )

        recommended_candidates = (
            additional_candidate_result.get(
                "recommended_candidates",
                []
            )
        )

        if recommended_candidates:

            for index, candidate in enumerate(
                recommended_candidates,
                start=1
            ):

                print(
                    f"\n#{index}"
                )

                print(
                    "Student:",
                    candidate.get(
                        "student_name",
                        candidate.get(
                            "student",
                            "Unknown"
                        )
                    )
                )

                print(
                    "Recommended Role:",
                    candidate.get(
                        "recommended_role",
                        "Not Available"
                    )
                )

                print(
                    "Matched Skill:",
                    candidate.get(
                        "matched_skill",
                        "Not Available"
                    )
                )

                print(
                    "Matched Role:",
                    candidate.get(
                        "matched_role",
                        "Not Available"
                    )
                )

                print(
                    "Score:",
                    candidate.get(
                        "ranking_score",
                        candidate.get(
                            "overall_score",
                            0
                        )
                    )
                )

        else:

            print(
                "No additional candidates found."
            )

        print(
            "\n=====================================================\n"
        )

    # ==========================================
    # STEP 7: SKILL GAP RESOLUTION
    # ==========================================

    skill_gap_resolver = SkillGapResolver()

    missing_skills = final_coverage.get(
        "missing_skills",
        []
    )

    skill_gap_report = (
        skill_gap_resolver.find_candidates(
            missing_skills,
            all_students,
            selected_team
        )
    )

    print(
        "\n========== SKILL GAP REPORT =========="
    )

    for gap in skill_gap_report:

        print(
            "\nMissing Skill:",
            gap.get(
                "missing_skill",
                "Unknown"
            )
        )

        print(
            "Status:",
            gap.get(
                "status",
                "Unknown"
            )
        )

        print(
            "Genuine Skill Gap:",
            gap.get(
                "is_genuine_gap",
                False
            )
        )

        print(
            "Best Candidate:",
            gap.get(
                "best_candidate",
                "None"
            )
        )

        print(
            "Recommendation:",
            gap.get(
                "recommendation",
                "No recommendation available."
            )
        )

    print(
        "\n======================================\n"
    )

    # ==========================================
    # FINAL RESPONSE
    # ==========================================

    return {
        "final_team": selected_team,
        "coverage": final_coverage,
        "skill_gaps": skill_gap_report,
        "additional_candidates": additional_candidate_result
    }