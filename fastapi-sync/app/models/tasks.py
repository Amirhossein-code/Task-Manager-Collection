import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class TaskStatus(enum.Enum):
    PENDING = "pending"
    ONGOING = "ongoing"
    DONE = "done"


class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    IMMEDIATE = "immediate"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(225), nullable=False)
    description = Column(String, nullable=True)

    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.LOW)

    # User provided
    start_time = Column(DateTime, nullable=False)
    finish_time = Column(DateTime, nullable=True)

    # Time Stamps
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(title='{self.title}', status='{self.status.name}', owner_id={self.owner_id})>"
