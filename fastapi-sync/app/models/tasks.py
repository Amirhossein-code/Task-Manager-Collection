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
    start_time = Column(DateTime(timezone=True), nullable=False)
    finish_time = Column(DateTime(timezone=True), nullable=True)

    # Time Stamps
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(title='{self.title}', status='{self.status.name}', owner_id={self.owner_id})>"


@event.listens_for(Task, "before_insert")
@event.listens_for(Task, "before_update")
def validate_task(mapper, connection, target):
    # Ensure both start_time and finish_time are timezone aware
    utc_timezone = pytz.utc

    if target.start_time is not None:
        if target.start_time.tzinfo is None:
            target.start_time = utc_timezone.localize(
                target.start_time
            )  # Make it aware in UTC

    if target.finish_time is not None:
        if target.finish_time.tzinfo is None:
            target.finish_time = utc_timezone.localize(
                target.finish_time
            )  # Make it aware in UTC

    # Perform the comparison only if both times are set
    if target.start_time is not None and target.finish_time is not None:
        if target.start_time >= target.finish_time:
            raise ValueError("finish_time must be greater than start_time")
