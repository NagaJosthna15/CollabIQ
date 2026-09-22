from database import invitations_collection


def get_student_invitations(student_id):
    invitations = list(
        invitations_collection.find(
            {
                "candidate_id": str(student_id)
            }
        ).sort(
            "created_at",
            -1
        )
    )

    result = []

    for invitation in invitations:
        result.append({
            "invitation_id": str(invitation["_id"]),
            "project_id": invitation["project_id"],
            "project_title": invitation["project_title"],
            "role": invitation["role"],
            "status": invitation["status"],
            "created_at": invitation.get("created_at"),
            "responded_at": invitation.get("responded_at")
        })

    return result


def get_student_accepted_projects(student_id):
    invitations = list(
        invitations_collection.find(
            {
                "candidate_id": str(student_id),
                "status": "accepted"
            }
        ).sort(
            "responded_at",
            -1
        )
    )

    result = []

    for invitation in invitations:
        result.append({
            "invitation_id": str(invitation["_id"]),
            "project_id": invitation["project_id"],
            "project_title": invitation["project_title"],
            "role": invitation["role"],
            "status": invitation["status"],
            "responded_at": invitation.get("responded_at")
        })

    return result
def get_project_candidate_status(project_id):
    invitations = list(
        invitations_collection.find(
            {
                "project_id": str(project_id)
            }
        ).sort(
            "created_at",
            -1
        )
    )

    latest_by_candidate = {}

    for invitation in invitations:
        candidate_id = str(
            invitation.get("candidate_id")
        )

        if candidate_id not in latest_by_candidate:
            latest_by_candidate[candidate_id] = invitation

    result = []

    counts = {
        "invited": 0,
        "accepted": 0,
        "rejected": 0,
        "expired": 0
    }

    for invitation in latest_by_candidate.values():
        status = invitation.get(
            "status",
            "invited"
        )

        if status in counts:
            counts[status] += 1

        result.append({
            "candidate_id": invitation.get(
                "candidate_id"
            ),
            "candidate_name": invitation.get(
                "candidate_name"
            ),
            "candidate_email": invitation.get(
                "candidate_email"
            ),
            "role": invitation.get(
                "role"
            ),
            "status": status,
            "invitation_id": str(
                invitation["_id"]
            ),
            "created_at": invitation.get(
                "created_at"
            ),
            "responded_at": invitation.get(
                "responded_at"
            )
        })

    return {
        "total_candidates": len(result),
        "invited": counts["invited"],
        "accepted": counts["accepted"],
        "rejected": counts["rejected"],
        "expired": counts["expired"],
        "candidates": result
    }