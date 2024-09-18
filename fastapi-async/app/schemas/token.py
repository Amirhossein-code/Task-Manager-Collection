from pydantic import BaseModel, EmailStr
from ..utils.auth.password_validators import ValidatedPassword


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class RequestResetPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    password: ValidatedPassword
