from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String(225), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(225), nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), default=func.now())
    last_updated = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    UniqueConstraint("email", name="uq_user_email")

    tasks = relationship("Task", back_populates="owner")
    password_reset_tokens = relationship("PasswordResetToken", back_populates="user")

    def __repr__(self):
        return f"<User: {self.full_name}>"
