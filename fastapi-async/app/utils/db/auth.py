from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status
from ...models import PasswordResetToken


async def create_password_reset_token(user_id: int, db: AsyncSession):
    token = str(uuid4())

    now = datetime.now(timezone.utc)
    expire_time = now + timedelta(minutes=5)
    expires_at = expire_time.isoformat().replace("+00:00", "Z")

    reset_token = PasswordResetToken(
        token=token, user_id=user_id, expires_at=expires_at
    )

    await db.add(reset_token)
    await db.commit()
    return token


async def retrieve_password_reset_token(token: str, db: AsyncSession):
    reset_token = await db.query(PasswordResetToken).filter_by(token=token).first()

    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    return reset_token


async def validate_password_reset_token(reset_token: PasswordResetToken):
    if reset_token.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has already been used",
        )

    now = datetime.now(timezone.utc)

    if reset_token.expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
        )

    return reset_token
