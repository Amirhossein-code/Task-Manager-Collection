from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from fastapi import HTTPException, status
from ...models import PasswordResetToken


def create_password_reset_token(user_id: int, db: Session):
    token = str(uuid4())

    now = datetime.now(timezone.utc)
    expire_time = now + timedelta(minutes=5)
    expires_at = expire_time.isoformat().replace("+00:00", "Z")

    reset_token = PasswordResetToken(
        token=token, user_id=user_id, expires_at=expires_at
    )
    db.add(reset_token)
    db.commit()
    return token


def retrieve_password_reset_token(token: str, db: Session):
    reset_token = db.query(PasswordResetToken).filter_by(token=token).first()
    return reset_token


def validate_password_reset_token(reset_token: PasswordResetToken):
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    if reset_token.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has already been used",
        )

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat().replace("+00:00", "Z")

    if reset_token.expires_at.isoformat() < now_iso[:-1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
        )

    return
