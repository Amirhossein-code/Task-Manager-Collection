from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...models import PasswordResetToken as PasswordResetTokenDBModel


async def create_password_reset_token(user_id: int, db: AsyncSession) -> str:
    # Generate a random token using uuid4
    token = str(uuid4())

    # Create desired time for password reset token expiry
    # now = datetime.now(timezone.utc)
    # expire_time = now + timedelta(minutes=settings.password_reset_token_expire_minutes)
    # expires_at = expire_time.isoformat().replace("+00:00", "Z")

    # Prep the data for a new password reset token instance
    reset_token = PasswordResetTokenDBModel(token=token, user_id=user_id)

    db.add(reset_token)
    await db.commit()

    return token


async def retrieve_password_reset_token(
    token: str, db: AsyncSession
) -> PasswordResetTokenDBModel:
    stmt = select(PasswordResetTokenDBModel).filter_by(token=token)
    result = await db.execute(stmt)
    reset_token = result.scalars().one_or_none()

    # Check if there is a token with the given token string
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Token Not Found"
        )

    return reset_token


async def validate_password_reset_token(
    reset_token: PasswordResetTokenDBModel,
) -> PasswordResetTokenDBModel:
    # Ensure token is not used
    if reset_token.is_used:
        raise HTTPException(
            detail="Token has already been used",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Ensure token is not expired
    now = datetime.now(timezone.utc)
    if reset_token.expires_at < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token has expired"
        )

    return reset_token
