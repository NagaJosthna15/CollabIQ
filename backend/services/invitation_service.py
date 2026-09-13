import secrets
from datetime import datetime, timezone

from database import invitations_collection
from services.email_service import send_project_invitation


def create_invitation(
    project_id,
    project_title,
    candidate,
    role,
    invitation_link
):
    profile = candidate.get("profile", candidate)

    candidate_id = (
        profile.get("student_id")
        or profile.get("_id")
    )

    candidate_name = (
        profile.get("student")
        or profile.get("name")
    )

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

    result = invitations_collection.insert_one(
        invitation
    )

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