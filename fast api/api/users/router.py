from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, crud

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/", response_model=schemas.UserDisplay, status_code=status.HTTP_201_CREATED
)
def sign_up(request: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(request.email, db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists!",
        )

    new_user = crud.create_new_user(request, db)
    return new_user


@router.get("/me", response_model=schemas.UserDisplay, status_code=status.HTTP_200_OK)
def get_logged_in_user(
    user: schemas.UserDisplay = Depends(crud.get_current_user_db),
):
    return user


@router.put("/me", response_model=schemas.UserDisplay, status_code=status.HTTP_200_OK)
def edit_logged_in_user_data(
    user_update: schemas.UserUpdate,
    user: schemas.UserDisplay = Depends(crud.get_current_user_db),
    db: Session = Depends(get_db),
):
    updated_user = crud.update_user(user, user_update, db)
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_logged_in_user(
    user: schemas.UserDisplay = Depends(crud.get_current_user_db),
    db: Session = Depends(get_db),
):
    crud.delete_user(user, db)
    return {"message": "User Deleted Successfully"}
