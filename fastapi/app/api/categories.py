from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

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
    db: AsyncSession = Depends(get_db_session),
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
    db: AsyncSession = (Depends(get_db_session)),
):
    category = await category_crud.get_category_by_id_or_404(
        category_id=category_id, db=db
    )

    if category.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this category",
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
    db: AsyncSession = Depends(get_db_session),
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
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    category_id: int,
    update_category_data: category_schemas.CategoryCreateUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    category = await category_crud.get_category_by_id_or_404(
        category_id=category_id, db=db
    )

    if category.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this Category",
        )

    updated_category = await category_crud.update_category(
        category=category,
        update_data=update_category_data,
        db=db,
    )

    return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    category_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    category = await category_crud.get_category_by_id_or_404(
        category_id=category_id, db=db
    )

    if category.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this category",
        )

    await category_crud.delete_category(category=category, db=db)

    return None
