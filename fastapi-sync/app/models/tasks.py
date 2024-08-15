import enum

import pytz
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    event,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    ONGOING = "ongoing"
    DONE = "done"


class TaskPriority(str, enum.Enum):
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
    start_time = Column(DateTime(timezone=True), nullable=True)
    finish_time = Column(DateTime(timezone=True), nullable=True)

    # Time Stamps
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(title='{self.title}', status='{self.status.name}', owner_id={self.owner_id})>"


@event.listens_for(Task, "before_update")
def validate_task_start_and_finish_time(mapper, connection, target):
    utc_timezone = pytz.utc

    if target.start_time is not None:
        if target.start_time.tzinfo is None:
            target.start_time = utc_timezone.localize(target.start_time)

    if target.finish_time is not None:
        if target.finish_time.tzinfo is None:
            target.finish_time = utc_timezone.localize(target.finish_time)

    if target.start_time is not None and target.finish_time is not None:
        if target.start_time >= target.finish_time:
            raise ValueError("database :finish_time must be greater than start_time")
