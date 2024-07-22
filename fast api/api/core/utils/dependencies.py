from fastapi import Depends
from sqlalchemy.orm import Session
from ...database import get_db
from ..schemas import users as user_schema
from .oauth2 import get_current_user
from ..services import UserCrud


def get_current_user_db_dependency(
    current_user: user_schema.UserValidate = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return UserCrud.get_user_or_404(current_user.email, db)
