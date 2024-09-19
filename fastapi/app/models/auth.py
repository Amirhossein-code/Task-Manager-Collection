from datetime import datetime, timedelta, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..core.config import settings
from ..core.database import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    is_used = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True))

    # relation ship with the User Model | Users can have multiple instances (1 to Many relationship)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="password_reset_tokens")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set expiration time
        self.expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.password_reset_token_expire_minutes
        )
