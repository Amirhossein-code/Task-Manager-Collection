from datetime import datetime, timedelta, timezone

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
)

from ..models.tasks import TaskPriority, TaskStatus


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    title: str
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    category_id: int
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
    category_id: int
    start_time: datetime | None = None
    finish_time: datetime | None = None

    @field_validator("status")
    def validate_status(cls, status: TaskStatus):
        if status == TaskStatus.DONE:
            raise ValueError("status cannot be Done at creation.")
        return status

    @field_validator("start_time")
    def validate_start_time(cls, start_time):
        if start_time is not None:
            last_acceptable_submit_time = datetime.now(timezone.utc) - timedelta(
                minutes=2
            )
            if start_time <= last_acceptable_submit_time:
                raise ValueError(
                    "start_time must be greater than the current time (give or take 2 minutes)."
                )

        return start_time

    @model_validator(mode="after")
    def validate_time_range(cls, instance):
        if instance.start_time and instance.finish_time:
            if instance.start_time >= instance.finish_time:
                raise ValueError("finish_time must be greater than start_time")
        return instance


class TaskUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = TaskStatus.PENDING
    priority: TaskPriority | None = TaskPriority.LOW
    category_id: int | None = None
    start_time: datetime | None = None
    finish_time: datetime | None = None

    @field_validator("start_time")
    def validate_start_time(cls, start_time):
        if start_time is not None:
            last_acceptable_submit_time = datetime.now(timezone.utc) - timedelta(
                minutes=2
            )
            if start_time <= last_acceptable_submit_time:
                raise ValueError(
                    "start_time must be greater than the current time (give or take 2 minutes)."
                )

        return start_time

    @model_validator(mode="after")
    def validate_time_range(cls, instance):
        if instance.start_time and instance.finish_time:
            if instance.start_time >= instance.finish_time:
                raise ValueError("finish_time must be greater than start_time")
        return instance
