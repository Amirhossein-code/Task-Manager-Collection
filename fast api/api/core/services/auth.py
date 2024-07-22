from pydantic import EmailStr
from sqlalchemy.orm import Session
from .hashing import Hash
from .users import UserCrud


def authenticate_user(db: Session, email: EmailStr, password: str):
    user = UserCrud.get_user_by_email(email=email)
    if not user:
        return False
    if not Hash.validate_password(password, user.hashed_password):
        return False
    return user
