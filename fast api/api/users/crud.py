from fastapi import HTTPException, status, Depends
from ..database import get_db
from ..auth.oauth2 import get_current_user
from sqlalchemy.orm import Session
from . import models, schemas
from .hashing import Hash


def get_user_by_email(email: str, db: Session):
    return db.query(models.User).filter(models.User.email == email).first()


def create_new_user(request: schemas.UserCreate, db: Session):
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


def update_user(user: models.User, user_update: schemas.UserUpdate, db: Session):
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(user: models.User, db: Session):
    db.delete(user)
    db.commit()
    return user


def get_user_or_404(email: str, db: Session):
    user = get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


# Dependency to get the current user from the database
def get_current_user_db(
    current_user: schemas.UserValidate = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_or_404(current_user.email, db)
