from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas import users as user_schemas
from ..utils.db import users as user_crud
from ..dependencies.get_active_user import get_current_active_user_db_dependency

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/", response_model=user_schemas.UserDisplay, status_code=status.HTTP_201_CREATED
)
def sign_up(request: user_schemas.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(request.email, db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists!",
        )

    new_user = user_crud.create_new_user(request, db)
    return new_user


@router.get(
    "/me", response_model=user_schemas.UserDisplay, status_code=status.HTTP_200_OK
)
def get_logged_in_user(
    user: user_schemas.UserDisplay = Depends(get_current_active_user_db_dependency),
):
    return user


@router.put(
    "/me", response_model=user_schemas.UserDisplay, status_code=status.HTTP_200_OK
)
def edit_logged_in_user_data(
    user_update: user_schemas.UserUpdate,
    user: user_schemas.UserDisplay = Depends(get_current_active_user_db_dependency),
    db: Session = Depends(get_db),
):
    updated_user = user_crud.update_user(user, user_update, db)
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_logged_in_user(
    user: user_schemas.UserDisplay = Depends(get_current_active_user_db_dependency),
    db: Session = Depends(get_db),
):
    user_crud.delete_user(user, db)
    return {"message": "User Deleted Successfully"}
