from typing import Annotated

from fastapi import Depends, HTTPException, status

from ..schemas import users as user_schemas
from ..utils.auth.authentication import get_current_user


async def get_current_active_user_db_dependency(
    user: Annotated[user_schemas.UserDisplay, Depends(get_current_user)],
):
    # Check if the user instance is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # return the current user
    return user
