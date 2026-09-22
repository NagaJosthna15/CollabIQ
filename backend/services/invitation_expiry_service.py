from datetime import datetime, timedelta, timezone

from database import invitations_collection


INVITATION_EXPIRY_HOURS = 48


def expire_pending_invitations(project_id=None):
    now = datetime.now(timezone.utc)

    expiry_time = now - timedelta(
        hours=INVITATION_EXPIRY_HOURS
    )

    query = {
        "status": "invited",
        "created_at": {
            "$lt": expiry_time
        }
    }

    if project_id:
        query["project_id"] = str(project_id)

    result = invitations_collection.update_many(
        query,
        {
            "$set": {
                "status": "expired",
                "responded_at": now
            }
        }
    )

    return {
        "success": True,
        "expired_count": result.modified_count,
        "checked_at": now,
        "expiry_hours": INVITATION_EXPIRY_HOURS,
        "project_id": str(project_id) if project_id else None
    }