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
