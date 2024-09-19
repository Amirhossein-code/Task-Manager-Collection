from typing import Annotated, List

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

from ..core.database import get_db_session
from ..dependencies import get_current_active_user_db_dependency
from ..schemas import categories as category_schemas
from ..schemas import users as user_schemas
from ..utils.db import categories as category_crud

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get(
    "/", response_model=List[category_schemas.Category], status_code=status.HTTP_200_OK
)
async def get_users_categories(
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    categories = await category_crud.get_user_categories(
        user=user,
        db=db,
    )

    return categories


@router.get(
    "/{category_id}",
    response_model=category_schemas.Category,
    status_code=status.HTTP_200_OK,
)
async def get_category_by_id(
    category_id: int,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    category = await category_crud.verify_category_ownership(
        user_id=user.id, category_id=category_id, db=db
    )

    return category


@router.post(
    "/",
    response_model=category_schemas.Category,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    request: category_schemas.CategoryCreateUpdate,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    new_category = await category_crud.create_category(
        request=request,
        user=user,
        db=db,
    )

    return new_category


@router.put(
    "/{category_id}",
    response_model=category_schemas.Category,
    status_code=status.HTTP_200_OK,
)
async def put_update_task(
    category_id: int,
    request: category_schemas.CategoryCreateUpdate,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    category = await category_crud.verify_category_ownership(
        user_id=user.id, category_id=category_id, db=db
    )

    updated_category = await category_crud.update_category(
        category=category,
        update_data=request,
        db=db,
    )

    return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    category_id: int,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    category = await category_crud.verify_category_ownership(
        user_id=user.id, category_id=category_id, db=db
    )

    await category_crud.delete_category(category=category, db=db)

    return None
