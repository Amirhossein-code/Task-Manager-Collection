from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

from ..utils.auth.password_validators import ValidatedPassword


class UserCreate(BaseModel):
    email: EmailStr
    password: ValidatedPassword
    full_name: str


class UserDisplay(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    full_name: str | None = None
    is_active: bool | None = None
    created_at: datetime
    last_updated: datetime


class UserValidate(BaseModel):
    email: EmailStr
    password: ValidatedPassword


class UserUpdate(BaseModel):
    full_name: str | None = None
