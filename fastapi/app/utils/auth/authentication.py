from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status

from ...core.config import settings
from ...core.database import get_db_session
from ...core.security import oauth2_scheme
from ...models import User as UserDBModel
from ...schemas import token as token_schema
from ...utils.auth import hashing
from ...utils.db import users as user_crud


async def authenticate_user(db: AsyncSession, email: EmailStr, password: str):
    # Check if the user exists
    user = await user_crud.get_user_by_email(email, db)
    if not user:
        return False

    # Check if the passwords match
    if not hashing.validate_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    # Set token expiry
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(settings.access_token_expire_minutes)
    )

    # Update data to include token expiry
    to_encode.update({"exp": expire})

    # Create the access token by encoding the data
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserDBModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )

        # check if the email is in the payload
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = token_schema.TokenData(email=email)

    except InvalidTokenError:
        raise credentials_exception

    # Retrieve the current user from the database
    user = await user_crud.get_user_by_email(email=token_data.email, db=db)
    if user is None:
        raise credentials_exception

    return user
