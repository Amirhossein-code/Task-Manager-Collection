from pydantic import BaseModel, ConfigDict
from ..models.tasks import TaskStatus, TaskPriority
from datetime import datetime


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    start_time: datetime
    finish_time: datetime


class TaskDetail(Task):
    time_created: datetime
    time_updated: datetime | None = None
    owner_id: int


class TaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.LOW
    start_time: datetime | None = None
    finish_time: datetime | None = None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = TaskStatus.PENDING
    priority: TaskPriority | None = TaskPriority.LOW
    start_time: datetime | None = None
    finish_time: datetime | None = None
