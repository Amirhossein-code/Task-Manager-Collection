import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import HTTPException, status

SMTP_SERVER = "smtp4dev"
SMTP_PORT = 25
SENDER_EMAIL = "noreply@example.com"
RESET_URL = "http://0.0.0.0:8000/reset-password"

logger = logging.getLogger(__name__)


def send_reset_email(to_email: str, token: str):
    subject = "Password Reset Request"
    body = f"Click the link to reset your password: {RESET_URL}?token={token}"

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)
        logger.info(f"Password reset email sent to {to_email}")
    except smtplib.SMTPException as e:
        logger.error(
            f"SMTP error occurred while sending reset password email to {to_email}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to send email due to SMTP error",
        )
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while sending reset password email to {to_email}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while sending email",
        )
