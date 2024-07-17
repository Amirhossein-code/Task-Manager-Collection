from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    full_name: str | None = None


class UserCreate(BaseUser):
    email: EmailStr
    password: str


class UserDisplay(BaseUser):
    email: EmailStr


class UserValidate(BaseModel):
    email: EmailStr
    password: str
