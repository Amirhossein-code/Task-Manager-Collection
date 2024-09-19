import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import send

from ...core.config import settings

logger = logging.getLogger(__name__)


async def send_reset_email(to_email: str, token: str) -> dict:
    """
    aiosmtplib is used so we can send email asynchronously
    """

    subject = "Password Reset Request"
    body = f"Click the link to reset your password: {settings.reset_callback_url}?token={token}"

    msg = MIMEMultipart()
    msg["From"] = settings.sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    await send(
        msg,
        hostname=settings.smtp_server,
        port=settings.smtp_port,
        # start_tls=True,
    )
    logger.info(f"Password reset email sent to {to_email}")
