from pydantic import BaseModel
from ..models.tasks import TaskStatus


class Task(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
