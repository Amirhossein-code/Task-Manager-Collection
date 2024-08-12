from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.security import oauth2_scheme
from ...core.config import settings
from ...schemas import token as token_schema
from ...utils.auth.hashing import Hash
from ...utils.db import users as user_crud


def authenticate_user(db: Session, email: EmailStr, password: str):
    user = user_crud.get_user_by_email(email, db)
    if not user:
        return False
    if not Hash.validate_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = token_schema.TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = user_crud.get_user_by_email(email=token_data.email, db=db)
    if user is None:
        raise credentials_exception

    return user
