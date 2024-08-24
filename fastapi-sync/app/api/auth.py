from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..schemas import token as token_schema
from ..utils.auth import authentication
from ..utils.auth.send_reset_password_email import send_reset_email
from ..utils.db import auth as auth_db
from ..utils.db import users as user_crud

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/token", response_model=token_schema.Token, status_code=status.HTTP_200_OK
)
def login_for_access_token(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authentication.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = authentication.create_access_token(
        data={
            "sub": user.email,
        }
    )
    return token_schema.Token(access_token=access_token, token_type="bearer")


@router.post("/request-reset-password")
def request_reset_password(
    request: token_schema.RequestResetPassword, db: Session = Depends(get_db)
):
    user = user_crud.get_user_by_email_or_404(email=request.email, db=db)

    token = auth_db.create_password_reset_token(user_id=user.id, db=db)

    send_reset_email(to_email=request.email, token=token)

    return {"message": "Password reset email sent. Check you email"}


@router.post("/reset-password")
def reset_password(
    request: token_schema.ResetPassword,
    password_reset_token: str = Query(...),
    db: Session = Depends(get_db),
):
    reset_token = auth_db.retrieve_password_reset_token(password_reset_token, db)
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )
    validated_reset_token = auth_db.validate_password_reset_token(reset_token)

    user = user_crud.get_user_by_id_or_404(user_id=validated_reset_token.user_id, db=db)

    user_crud.reset_user_password(user, request.password, db)
    validated_reset_token.is_used = True
    db.commit()

    return {"message": "Password reset successfully."}
