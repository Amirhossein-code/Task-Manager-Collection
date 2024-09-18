import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import send
from ...core.config import settings

logger = logging.getLogger(__name__)


async def send_reset_email(to_email: str, token: str):
    subject = "Password Reset Request"
    body = f"Click the link to reset your password: {settings.reset_callback_url}?token={token}"

    msg = MIMEMultipart()
    msg["From"] = settings.sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        await send(
            msg,
            hostname=settings.smtp_server,
            port=settings.smtp_port,
            start_tls=True,  # If you're using TLS
        )
        logger.info(f"Password reset email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}", exc_info=True)
