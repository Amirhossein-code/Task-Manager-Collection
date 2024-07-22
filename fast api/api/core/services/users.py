from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import users as user_schema
from .hashing import Hash
from pydantic import EmailStr


class UserCrud:
    @staticmethod
    def get_user_by_email(email: EmailStr, db: Session) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_or_404(email: EmailStr, db: Session):
        user = UserCrud.get_user_by_email(email, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    @staticmethod
    def create_new_user(request: user_schema.UserCreate, db: Session):
        hashed_password = Hash.hash_password(password=request.password)
        new_user = User(
            email=request.email,
            hashed_password=hashed_password,
            full_name=request.full_name,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_user(user: User, user_update: user_schema.UserUpdate, db: Session):
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(user: User, db: Session):
        try:
            db.delete(user)
            db.commit()
            return {"message": "User deleted successfully"}
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the user",
            )
