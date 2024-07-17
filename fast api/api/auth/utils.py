import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from ..users import models
from ..users.hashing import Hash
from ..settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from pydantic import EmailStr


def authenticate_user(db: Session, email: EmailStr, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not Hash.validate_password(
        password,
        user.hashed_password,
    ):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
