from pydantic import BaseModel, EmailStr, ConfigDict
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


class UserValidate(BaseModel):
    email: EmailStr
    password: ValidatedPassword


class UserUpdate(BaseModel):
    full_name: str | None = None
