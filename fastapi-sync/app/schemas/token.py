from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None


class ResetPassword(BaseModel):
    email: EmailStr
