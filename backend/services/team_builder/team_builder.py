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
    pass   


def build_team(
    project_requirements,
    ranked_candidates
):

    preferred_roles = project_requirements.get(
        "preferred_roles",
        []
    )

    selected_team = []

    used_students = set()

    for role in preferred_roles:

        print("\nSearching for role:", role)
        best_candidate = None
        best_similarity = 0

        for candidate in ranked_candidates:

            profile = candidate["profile"]
            similarity = role_similarity(
                role, 
                profile["recommended_role"]
                )
            if similarity > best_similarity:
                 best_similarity = similarity
                 best_candidate = candidate
            skill_score = candidate["scores"]["skill"]
            ranking_score = candidate["scores"]["final"]
            print(
                profile["student"],
                "| Role:",
                profile["recommended_role"],
                "| Similarity:",
                similarity,
                "| Skill:",
                skill_score,
                "| Ranking:",
                ranking_score
            )
        if best_candidate is not None:
            print(
                "Selected:",

                 best_candidate["profile"]["student"]
        )
         

      
            

    return selected_team