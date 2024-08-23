import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import HTTPException

SMTP_SERVER = "smtp4dev"
SMTP_PORT = 25
SENDER_EMAIL = "noreply@example.com"

logger = logging.getLogger(__name__)


def send_reset_email(to_email: str, token: str):
    subject = "Password Reset Request"
    body = f"Click the link to reset your password: http://0.0.0.0:8000/reset-password?token={token}"

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)
    except smtplib.SMTPException as e:
        logger.error(
            f"SMTP error occurred while sending reset password email to {to_email}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Failed to send email")
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while sending reset password email to {to_email}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Failed to send email")
