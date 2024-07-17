from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..users import schemas as user_schemas
from .utils import authenticate_user, create_access_token
from .schemas import Token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/token")
def login_for_access_token(
    request: user_schemas.UserValidate, db: Session = Depends(get_db)
):
    user = authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={
            "sub": user.email,
        }
    )
    return Token(access_token=access_token, token_type="bearer")
