from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
import enum


class TaskStatus(enum.Enum):
    PENDING = "pending"
    ONGOING = "ongoing"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(225), nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    start_time = Column(DateTime, nullable=False)
    finish_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    last_updated = Column(
        DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship to the User model
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<User: {self.full_name}>"
