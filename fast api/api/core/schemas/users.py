from pydantic import BaseModel, EmailStr
from ..services.password_validators import ValidatedPassword


class UserBase(BaseModel):
    full_name: str | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: ValidatedPassword


class UserDisplay(UserBase):
    email: EmailStr

    class Config:
        from_attributes = True


class UserValidate(BaseModel):
    email: EmailStr
    password: ValidatedPassword


class UserUpdate(UserBase):
    class Config:
        from_attributes = True
