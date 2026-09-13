from services.email_service import send_project_invitation
import os

result = send_project_invitation(
    candidate_email=os.getenv("EMAIL_ADDRESS"),
    candidate_name="CollabIQ Test",
    project_title="CollabIQ Email Test",
    role="Test Candidate",
    invitation_link="http://127.0.0.1:8000"
)

print(result)