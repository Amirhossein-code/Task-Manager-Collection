from datetime import datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

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
