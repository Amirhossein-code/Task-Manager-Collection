from ..core.database import get_db
from ..core.security import get_current_user
from fastapi import Depends
from sqlalchemy.orm import Session
from ..utils.db import users as user_crud

from ..schemas import users as user_schemas


def get_current_user_db_dependency(
    current_user: user_schemas.UserValidate = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_crud.get_user_or_404(current_user.email, db)
