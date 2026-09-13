import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

def send_project_invitation(
    candidate_email,
    candidate_name,
    project_title,
    role,
    invitation_link
):
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        raise ValueError("Email configuration is missing")

    message = EmailMessage()

    message["Subject"] = f"CollabIQ Project Invitation - {project_title}"
    message["From"] = EMAIL_ADDRESS
    message["To"] = candidate_email

    message.set_content(
        f"""Hi {candidate_name},

You have been selected for the project "{project_title}" as a {role}.

Your profile and skills were identified as a strong match for this project.

If you are interested in joining the project, please review the invitation and choose Accept or Reject:

{invitation_link}

Regards,
CollabIQ Recruitment Team
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD
        )
        server.send_message(message)

    return {
        "success": True,
        "message": "Project invitation email sent successfully"
    }