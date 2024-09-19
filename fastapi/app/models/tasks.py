import enum
from datetime import datetime, timezone

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

    # Enums
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.LOW)

    # User provided
    start_time = Column(DateTime(timezone=True), nullable=True)
    finish_time = Column(DateTime(timezone=True), nullable=True)

    # Time Stamps
    time_created = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.now(timezone.utc))

    # User model relationship | Users can create many tasks (1 to Many relationship)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="tasks")

    # Category model relationship
    # A category can have many tasks and each task must have a category (1 to Many relationship)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="tasks")

    def __repr__(self):
        return f"<Task(title='{self.title}')>"


@event.listens_for(Task, "before_update")
def validate_task_start_and_finish_time(mapper, connection, target):
    """
    Validate the start and finish times of a Task instance before updating.

    This function ensures that:
    - Start and finish times are localized to UTC if they are naive (i.e., without timezone info).
    - The finish time must be greater than the start time.

    These validations are enforced at the database level to complement checks performed
    by Pydantic during task creation.
    At update unlike create we need database access to enforce the rules
    """
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


"""  
Summary of Rules for Task Start and Finish Times:  

1. **Task Creation (`TaskCreate` Class)**:  
    - **Start Time Validation**:  
        - If `start_time` is provided, it must be greater than the current time (with a tolerance of 2 minutes).
            This prevents scheduling tasks in the past.  
    - **Finish Time Validation**:  
        - If both `start_time` and `finish_time` are provided, `finish_time` must be greater than `start_time`.
            This ensures that a task cannot finish before it starts.  

2. **Task Update (`TaskUpdate` Class)**:  
    - **Start Time Validation**:  
        - If `start_time` is provided, it must also be greater than the current time (with a tolerance of 2 minutes).  
    - **Finish Time Validation**:  
        - If both `start_time` and `finish_time` are provided, `finish_time` must be greater than `start_time`.
            This rule maintains logical consistency in task scheduling.  

3. **Database-Level Validation (`validate_task_start_and_finish_time` Event Listener)**:  
    - **Timezone Localization**:  
        - If `start_time` or `finish_time` are naive (without timezone information) before updating a task,
            they are localized to UTC.  
    - **Finish Time Validation**:  
        - If both `start_time` and `finish_time` are present, `finish_time` must be greater than `start_time`. 
        This validation is enforced at the database level to ensure data integrity, particularly when updating existing records.  

These rules ensure valid and logical time settings for all tasks, preventing scheduling conflicts and 
maintaining data integrity throughout the task lifecycle.  
"""
