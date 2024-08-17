from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import timedelta, datetime

from ..core.database import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="password_reset_tokens")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.created_at:
            self.expires_at = self.created_at + timedelta(minutes=5)
        else:
            self.expires_at = datetime.now() + timedelta(minutes=5)
