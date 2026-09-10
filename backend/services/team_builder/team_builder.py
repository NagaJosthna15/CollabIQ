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


# ============================================================
# PRIMARY ROLE ASSIGNMENT
# ============================================================

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
                ),
                "selection_type": "primary"
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


# ============================================================
# SECONDARY ROLE ASSIGNMENT
# ============================================================

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

            candidate = member.get(
                "candidate",
                {}
            )

            profile = candidate.get(
                "profile",
                {}
            )

            student_name = profile.get(
                "student"
            )

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



def convert_additional_candidate_to_team_member(candidate):

    profile = candidate.get(
        "profile",
        {}
    )

    student_name = (
        candidate.get("student_name")
        or candidate.get("student")
        or profile.get("student")
        or profile.get("name")
        or "Unknown"
    )

    recommended_role = candidate.get(
        "recommended_role",
        "Unknown"
    )

    ranking_score = candidate.get(
        "ranking_score",
        candidate.get(
            "overall_score",
            0
        )
    )

    # Make sure profile has student name
    if not isinstance(profile, dict):
        profile = {}

    if "student" not in profile:
        profile["student"] = student_name

    if "recommended_role" not in profile:
        profile["recommended_role"] = recommended_role

    return {
        "role": recommended_role,

        "candidate": {
            "profile": profile,

            "scores": {
                "final": ranking_score,

                "skill": candidate.get(
                    "skill_similarity",
                    0
                ),

                "role": candidate.get(
                    "role_similarity",
                    0
                )
            }
        },

        "selection_score": ranking_score,

        "selection_type": "additional",

        "matched_skill": candidate.get(
            "matched_skill"
        ),

        "matched_role": candidate.get(
            "matched_role"
        )
    }

def build_team(
    project_requirements,
    ranked_candidates
):

  
    primary_result = assign_primary_roles(
        project_requirements,
        ranked_candidates
    )

    selected_team = primary_result.get(
        "selected_team",
        []
    )

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

    missing_roles = initial_coverage.get(
        "missing_roles",
        []
    )

    selected_team = assign_secondary_roles(
        project_requirements,
        selected_team,
        missing_roles
    )


    coverage_after_secondary = coverage_analyzer.analyze(
        project_requirements,
        selected_team
    )

    remaining_roles = coverage_after_secondary.get(
        "missing_roles",
        []
    )

    remaining_skills = coverage_after_secondary.get(
        "missing_skills",
        []
    )

    print(
        "\n========== COVERAGE AFTER SECONDARY ROLES =========="
    )

    print(
        "Remaining Roles:",
        remaining_roles
    )

    print(
        "Remaining Skills:",
        remaining_skills
    )

    print(
        "====================================================\n"
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

    additional_candidates = []

    if remaining_roles or remaining_skills:

        print(
            "\n========== ADDITIONAL CANDIDATE SELECTION =========="
        )

        all_students = get_all_students()

        additional_selector = (
            AdditionalCandidateSelector()
        )

        current_team_profiles = []

        for member in selected_team:

            candidate = member.get(
                "candidate",
                {}
            )

            profile = candidate.get(
                "profile",
                {}
            )

            if profile:

                current_team_profiles.append(
                    profile
                )

        # Decide number of additional candidates needed
        number_needed = len(
            remaining_roles
        )

        # If there are no missing roles but skills are missing,
        # allow up to 3 additional candidates
        if number_needed == 0 and remaining_skills:

            number_needed = min(
                3,
                len(remaining_skills)
            )

        # Maximum additional candidates
        number_needed = min(
            number_needed,
            4
        )

        additional_requirements = {

            "skills": remaining_skills,

            "roles": remaining_roles,

            "preferred_roles": remaining_roles
        }

        additional_candidate_result = (
            additional_selector.select_candidates(
                project_requirements=additional_requirements,
                current_team=current_team_profiles,
                all_students=all_students,
                number_needed=number_needed
            )
        )

        additional_candidates = (
            additional_candidate_result.get(
                "recommended_candidates",
                []
            )
        )

        print(
            "Members Requested:",
            number_needed
        )

        print(
            "Additional Candidates Found:",
            len(additional_candidates)
        )


      

        for candidate in additional_candidates:

            team_member = (
                convert_additional_candidate_to_team_member(
                    candidate
                )
            )

            selected_team.append(
                team_member
            )

            student_name = candidate.get(
                "student_name"
            ) or candidate.get(
                "student",
                "Unknown"
            )

            print(
                "Added:",
                student_name,
                "| Role:",
                candidate.get(
                    "recommended_role",
                    "Unknown"
                ),
                "| Matched Role:",
                candidate.get(
                    "matched_role",
                    "None"
                ),
                "| Matched Skill:",
                candidate.get(
                    "matched_skill",
                    "None"
                )
            )

        print(
            "\n====================================================\n"
        )


  
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
    skill_gap_resolver = SkillGapResolver()

    all_students = get_all_students()

    final_missing_skills = final_coverage.get(
        "missing_skills",
        []
    )

    skill_gap_report = (
        skill_gap_resolver.find_candidates(
            final_missing_skills,
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


    # ========================================================
    # FINAL RETURN
    # ========================================================

    return {

        "final_team": selected_team,

        "coverage": final_coverage,

        "skill_gaps": skill_gap_report,

        "additional_candidates": additional_candidates,

        "additional_candidate_result":
            additional_candidate_result
    }