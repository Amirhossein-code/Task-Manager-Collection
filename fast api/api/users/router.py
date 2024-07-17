from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from . import schemas, crud


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
