from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
)


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str


class CategoryDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    time_created: datetime | None = None
    time_updated: datetime | None = None
