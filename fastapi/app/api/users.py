from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from ..core.database import get_db_session
from ..dependencies.get_active_user import get_current_active_user_db_dependency

from ..schemas import users as user_schemas
from ..utils.db import users as user_crud

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/", response_model=user_schemas.UserDisplay, status_code=status.HTTP_201_CREATED
)
async def sign_up(
    user_data: user_schemas.UserCreate,
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    new_user = await user_crud.create_new_user(user_data=user_data, db=db)
    return new_user


@router.get(
    "/me", response_model=user_schemas.UserDisplay, status_code=status.HTTP_200_OK
)
async def get_logged_in_user(
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
):
    return user


@router.put(
    "/me", response_model=user_schemas.UserDisplay, status_code=status.HTTP_200_OK
)
async def put_logged_in_user(
    update_data: user_schemas.UserUpdate,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    updated_user = await user_crud.update_user(
        user=user, update_data=update_data, db=db, full_update=True
    )
    return updated_user


@router.patch(
    "/me", response_model=user_schemas.UserDisplay, status_code=status.HTTP_200_OK
)
async def patch_logged_in_user(
    update_data: user_schemas.UserUpdate,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    updated_user = await user_crud.update_user(
        user=user, update_data=update_data, db=db, full_update=False
    )
    return updated_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_logged_in_user(
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    await user_crud.delete_user(user=user, db=db)
    return None
