from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db_session
from ..dependencies import get_current_active_user_db_dependency
from ..schemas import categories as category_schemas, users as user_schemas
from ..utils.db import categories as category_crud

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.post(
    "/", response_model=category_schemas.Category, status_code=status.HTTP_201_CREATED
)
async def create_category(
    request: category_schemas.Category,
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
