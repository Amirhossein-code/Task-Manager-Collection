from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str
