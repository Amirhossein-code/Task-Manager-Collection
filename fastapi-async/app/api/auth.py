import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db_session
from ..schemas import token as token_schema
from ..utils.auth import authentication
from ..utils.auth.send_reset_password_email import send_reset_email
from ..utils.db import auth as auth_db
from ..utils.db import users as user_crud

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/token", response_model=token_schema.Token, status_code=status.HTTP_200_OK
)
async def login_for_access_token(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    user = await authentication.authenticate_user(
        db, request.username, request.password
    )
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
async def request_reset_password(
    request: token_schema.RequestResetPassword,
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    user = await user_crud.get_user_by_email_or_404(email=request.email, db=db)

    token = await auth_db.create_password_reset_token(user_id=user.id, db=db)

    try:
        await send_reset_email(to_email=request.email, token=token)
    except Exception as e:
        logger.error(f"Failed to send email to {request.email}: {e}", exc_info=True)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send password reset email.",
        )

    return {"message" : "Email Sent Successfully"}


@router.post("/reset-password")
async def reset_password(
    request: token_schema.ResetPassword,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    password_reset_token: str = Query(...),
):
    reset_token = await auth_db.retrieve_password_reset_token(password_reset_token, db)
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
        )

    validated_reset_token = await auth_db.validate_password_reset_token(reset_token)
    user = await user_crud.get_user_by_id_or_404(
        user_id=validated_reset_token.user_id, db=db
    )

    await user_crud.reset_user_password(user, request.password, db)
    validated_reset_token.is_used = True
    await db.commit()

    return {"message": "Password reset successfully."}
