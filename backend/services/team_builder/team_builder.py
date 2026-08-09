from services.agents.responsibility_agent import (
    ResponsibilityAgent
)

from services.matching.semantic_role_matcher import (
    role_similarity
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

            profile = candidate["profile"]

            student_name = profile["student"]

            # Do not assign the same student
            # to multiple primary roles
            if student_name in used_students:
                continue

            # --------------------------------
            # 1. Semantic Role Similarity
            # --------------------------------

            similarity = role_similarity(
                role,
                profile["recommended_role"]
            )

            # --------------------------------
            # 2. Skill Score
            # --------------------------------

            skill_score = candidate["scores"].get(
                "skill",
                0
            )

            # --------------------------------
            # 3. Overall Candidate Ranking
            # --------------------------------

            ranking_score = candidate["scores"].get(
                "final",
                0
            )

            # --------------------------------
            # Combined Primary Role Score
            # --------------------------------

            combined_score = (
                (similarity * 40)
                + (skill_score * 0.35)
                + (ranking_score * 0.25)
            )

            print(
                profile["student"],
                "| Role:",
                profile["recommended_role"],
                "| Similarity:",
                round(similarity, 2),
                "| Skill:",
                skill_score,
                "| Ranking:",
                ranking_score,
                "| Combined:",
                round(combined_score, 2)
            )

            # --------------------------------
            # Select best candidate
            # --------------------------------

            if combined_score > best_score:

                best_score = combined_score

                best_candidate = candidate

        # --------------------------------
        # Assign Primary Role
        # --------------------------------

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

    primary_result = assign_primary_roles(
        project_requirements,
        ranked_candidates
    )

    selected_team = primary_result[
        "selected_team"
    ]

    unassigned_roles = primary_result[
        "unassigned_roles"
    ]

    selected_team = assign_secondary_roles(
        project_requirements,
        selected_team,
        unassigned_roles
    )

    return selected_team