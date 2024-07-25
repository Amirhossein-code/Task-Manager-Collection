from ..core.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String(225), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(225), nullable=False)
    is_active = Column(Boolean, default=False)

    UniqueConstraint("email", name="uq_user_email")

    tasks = relationship("Task", back_populates="owner")

    def __repr__(self):
        return f"<User: {self.full_name}>"
