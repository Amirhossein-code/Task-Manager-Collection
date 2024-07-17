from fastapi import APIRouter, Depends, HTTPException, status ,Response
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, crud
from ..auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=schemas.UserDisplay)
def sign_up(request: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(request.email, db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists!",
        )

    new_user = crud.create_new_user(request, db)

    return new_user


@router.get("/me", response_model=schemas.UserDisplay)
def get_logged_in_user(
    current_user: schemas.UserValidate = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(current_user.email, db)
    return user


@router.put("/me", response_model=schemas.UserDisplay)
def edit_logged_in_user_data(
    user_update: schemas.UserUpdate,
    current_user: schemas.UserValidate = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(current_user.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    updated_user = crud.update_user(user, user_update, db)
    return updated_user


@router.delete("/me")
def delete_logged_in_user(
    current_user: schemas.UserValidate = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(current_user.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    crud.delete_user(user, db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
