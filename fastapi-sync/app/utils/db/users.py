import logging

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ...models import User
from ...schemas import users as user_schemas
from ..auth.hashing import Hash

logger = logging.getLogger(__name__)


def get_user_by_email(email: EmailStr, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


def get_user_by_email_or_404(email: EmailStr, db: Session) -> User:
    try:
        user = get_user_by_email(email, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
    except HTTPException as http_exec:
        raise http_exec
    except SQLAlchemyError as e:
        logger.error(
            f"Database error while retrieving user with email {email}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while retrieving the user.",
        )
    except Exception as e:
        logger.error(f"Unexpected error while retrieving user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the user.",
        )


def create_new_user(user_data: user_schemas.UserCreate, db: Session) -> User:
    try:
        existing_user = get_user_by_email(user_data.email, db)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
            )

        hashed_password = Hash.hash_password(password=user_data.password)

        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except HTTPException as http_exec:
        raise http_exec

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while creating new user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while creating a new user.",
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user.",
        )


def update_user(
    user: User,
    update_data: user_schemas.UserUpdate,
    db: Session,
    full_update: bool,  # True -> PUT | False -> Patch
) -> User:
    try:
        data_to_update = update_data.model_dump(exclude_unset=not full_update)
        for key, value in data_to_update.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(
            f"Database error while updating user with ID {user.id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while updating the user.",
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while updating user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the user.",
        )


def delete_user(user: User, db: Session) -> None:
    try:
        db.delete(user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(
            f"Database error while deleting user with ID {user.id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while deleting the user.",
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while deleting user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the user.",
        )
