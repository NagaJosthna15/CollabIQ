from services.agents.responsibility_agent import (
    ResponsibilityAgent
)
from services.matching.semantic_role_matcher import (
    role_similarity
)
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

        print("\nSearching:", role)

        best_candidate = None
        best_similarity = 0

        for candidate in ranked_candidates:

            profile = candidate["profile"]

            student_name = profile["student"]

            if student_name in used_students:
                continue

            similarity = role_similarity(
                role,
                profile["recommended_role"]
            )

            if similarity > best_similarity:

                best_similarity = similarity
                best_candidate = candidate

        if best_candidate is not None:

            selected_team.append({
                "role": role,
                "candidate": best_candidate
            })

            used_students.add(
                best_candidate["profile"]["student"]
            )

        else:

            unassigned_roles.append(role)

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