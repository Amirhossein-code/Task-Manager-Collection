from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..schemas import users as user_schema
from .hashing import Hash
from pydantic import EmailStr


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_or_404(db: Session, email: EmailStr):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def create_new_user(request: user_schema.UserCreate, db: Session):
    hashed_password = Hash.hash_password(password=request.password)
    new_user = models.User(
        email=request.email,
        hashed_password=hashed_password,
        full_name=request.full_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(user: models.User, user_update: user_schema.UserUpdate, db: Session):
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(user: models.User, db: Session):
    db.delete(user)
    db.commit()
    return user
