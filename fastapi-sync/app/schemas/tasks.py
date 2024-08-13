from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..models.tasks import TaskPriority, TaskStatus


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    start_time: datetime | None = None
    finish_time: datetime | None = None


class TaskDetail(Task):
    time_created: datetime
    time_updated: datetime | None = None
    owner_id: int


class TaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.LOW
    start_time: datetime | None = None
    finish_time: datetime | None = None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = TaskStatus.PENDING
    priority: TaskPriority | None = TaskPriority.LOW
    start_time: datetime | None = None
    finish_time: datetime | None = None
