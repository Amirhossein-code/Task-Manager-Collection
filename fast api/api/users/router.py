from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from .crud import UserCrud
from .schemas import users

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=users.User)
def create_user(user: users.UserCreate, db: Session = Depends(get_db)):
    crud = UserCrud(db)
    db_user = crud.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(user)
