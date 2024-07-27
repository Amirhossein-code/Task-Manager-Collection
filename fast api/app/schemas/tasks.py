from pydantic import BaseModel
from ..models.tasks import TaskStatus
from datetime import datetime


class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: TaskStatus
    time_created: datetime
    time_updated: datetime | None = None
    owner_id: int

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
