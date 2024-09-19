from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from ..core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)

    # Email is required for authentication; username is not needed.
    email = Column(String(225), nullable=False, unique=True)

    # Stores the hashed password to ensure security; plain passwords are not stored.
    hashed_password = Column(String, nullable=False)

    # Indicates whether the user account is active; can be used to disable access.
    is_active = Column(Boolean, default=True)

    # Full name of the user for display purposes.
    full_name = Column(String(225), nullable=False)

    # Time Stamps
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    last_updated = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    UniqueConstraint("email", name="uq_user_email")

    # Relationship to other models
    tasks = relationship("Task", back_populates="owner")
    categories = relationship("Category", back_populates="owner")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")

    def __repr__(self):
        return f"<User: {self.full_name}>"
