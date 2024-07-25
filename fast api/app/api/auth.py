from ..core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas import token as token_schema
from ..utils.auth import token as token_utils

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/token")
def login_for_access_token(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = token_utils.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = token_utils.create_access_token(
        data={
            "sub": user.email,
        }
    )
    return token_schema(access_token=access_token, token_type="bearer")
