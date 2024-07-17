from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserDisplay(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None

    class Config:
        orm_mode = True


class UserValidate(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: str = None
    is_active: bool = None

    class Config:
        orm_mode = True
