import secrets
from datetime import datetime, timezone

from database import invitations_collection
from services.email_service import send_project_invitation
from services.invitation_replacement_service import find_replacement_candidate


def create_invitation(
    project_id,
    project_title,
    candidate,
    role,
    invitation_link
):
    profile = candidate.get("profile", {})

    candidate_id = (
        profile.get("student_id")
        or profile.get("_id")
        or profile.get("id")
    )
    candidate_name = profile.get("student") or profile.get("name")
    candidate_email = profile.get("email")

    if not candidate_id:
        raise ValueError("Candidate ID is missing")

    if not candidate_name:
        raise ValueError("Candidate name is missing")

    if not candidate_email:
        raise ValueError("Candidate email is missing")

    token = secrets.token_urlsafe(32)

    invitation = {
        "project_id": str(project_id),
        "project_title": project_title,
        "candidate_id": str(candidate_id),
        "candidate_name": candidate_name,
        "candidate_email": candidate_email,
        "role": role,
        "token": token,
        "status": "invited",
        "created_at": datetime.now(timezone.utc),
        "responded_at": None
    }

    try:
        result = invitations_collection.insert_one(
            invitation
        )
    except Exception as e:
        raise RuntimeError(
            "Database service is temporarily unavailable"
        ) from e

    link = f"{invitation_link}?token={token}"

    send_project_invitation(
        candidate_email=candidate_email,
        candidate_name=candidate_name,
        project_title=project_title,
        role=role,
        invitation_link=link
    )

    invitation["_id"] = str(result.inserted_id)

    return invitation


def accept_invitation(token):
    try:
        invitation = invitations_collection.find_one({
            "token": token
        })
    except Exception as e:
        raise RuntimeError(
            "Database service is temporarily unavailable"
        ) from e

    if not invitation:
        return {
            "success": False,
            "message": "Invitation not found"
        }

    if invitation.get("status") != "invited":
        return {
            "success": False,
            "message": f"Invitation already {invitation.get('status')}"
        }

    responded_at = datetime.now(timezone.utc)

    try:
        invitations_collection.update_one(
            {
                "_id": invitation["_id"]
            },
            {
                "$set": {
                    "status": "accepted",
                    "responded_at": responded_at
                }
            }
        )
    except Exception as e:
        raise RuntimeError(
            "Database service is temporarily unavailable"
        ) from e

    return {
        "success": True,
        "message": "Invitation accepted successfully",
        "candidate_name": invitation["candidate_name"],
        "project_title": invitation["project_title"],
        "role": invitation["role"],
        "status": "accepted",
        "responded_at": responded_at
    }


def reject_invitation(token):
    try:
        invitation = invitations_collection.find_one({
            "token": token
        })
    except Exception as e:
        raise RuntimeError(
            "Database service is temporarily unavailable"
        ) from e

    if not invitation:
        return {
            "success": False,
            "message": "Invitation not found"
        }

    if invitation.get("status") != "invited":
        return {
            "success": False,
            "message": f"Invitation already {invitation.get('status')}"
        }

    responded_at = datetime.now(timezone.utc)

    try:
        invitations_collection.update_one(
            {
                "_id": invitation["_id"]
            },
            {
                "$set": {
                    "status": "rejected",
                    "responded_at": responded_at
                }
            }
        )
    except Exception as e:
        raise RuntimeError(
            "Database service is temporarily unavailable"
        ) from e

    try:
        existing_invitations = invitations_collection.find({
            "project_id": invitation["project_id"]
        })

        excluded_candidate_ids = set()

        for existing in existing_invitations:
            candidate_id = existing.get("candidate_id")

            if candidate_id:
                excluded_candidate_ids.add(
                    str(candidate_id)
                )
    except Exception as e:
        raise RuntimeError(
            "Database service is temporarily unavailable"
        ) from e

    replacement = find_replacement_candidate(
        project_id=invitation["project_id"],
        role=invitation["role"],
        excluded_candidate_ids=excluded_candidate_ids
    )

    replacement_result = None

    if replacement:
        replacement_id = str(
            replacement.get("_id")
        )

        replacement_name = (
            replacement.get("student")
            or replacement.get("name")
        )

        replacement_email = replacement.get(
            "email"
        )

        replacement_profile = {
            "student_id": replacement_id,
            "student": replacement_name,
            "email": replacement_email,
            "skills": replacement.get(
                "skills",
                []
            ),
            "resume_skills": replacement.get(
                "resume_skills",
                []
            ),
            "recommended_role": replacement.get(
                "recommended_role"
            )
        }

        replacement_candidate = {
            "profile": replacement_profile
        }

        replacement_invitation = create_invitation(
            project_id=invitation["project_id"],
            project_title=invitation["project_title"],
            candidate=replacement_candidate,
            role=invitation["role"],
            invitation_link="http://127.0.0.1:8000/invitations/respond"
        )

        replacement_result = {
            "candidate_name": replacement_invitation[
                "candidate_name"
            ],
            "candidate_email": replacement_invitation[
                "candidate_email"
            ],
            "role": replacement_invitation[
                "role"
            ],
            "status": replacement_invitation[
                "status"
            ],
            "invitation_id": replacement_invitation[
                "_id"
            ]
        }

    return {
        "success": True,
        "message": "Invitation rejected successfully",
        "candidate_name": invitation["candidate_name"],
        "project_title": invitation["project_title"],
        "role": invitation["role"],
        "status": "rejected",
        "responded_at": responded_at,
        "replacement": replacement_result
    }