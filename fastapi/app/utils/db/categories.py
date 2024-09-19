from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...models import Category as CategoryDBModel, User as UserDBModel
from ...schemas import categories as category_schemas


async def create_category(
    request: category_schemas.CategoryCreateUpdate,
    user: UserDBModel,
    db: AsyncSession,
) -> CategoryDBModel:
    category_data = request.model_dump()
    category = CategoryDBModel(**category_data, owner_id=user.id)

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


async def get_category_by_id(category_id: int, db: AsyncSession) -> CategoryDBModel:
    stmt = select(CategoryDBModel).filter(CategoryDBModel.id == category_id)
    result = await db.execute(stmt)
    category = result.scalars().one_or_none()

    return category


async def get_category_by_id_or_404(
    category_id: int, db: AsyncSession
) -> CategoryDBModel:
    category = await get_category_by_id(category_id=category_id, db=db)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    return category


async def get_user_categories(
    user: UserDBModel, db: AsyncSession
) -> category_schemas.Category:
    stmt = select(CategoryDBModel).filter(CategoryDBModel.owner_id == user.id)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    return categories


async def update_category(
    category: CategoryDBModel,
    update_data: category_schemas.CategoryCreateUpdate,
    db: AsyncSession,
) -> CategoryDBModel:
    # Creates a dictionary representation of a category data (Pydantic model instance)
    data_to_update = update_data.model_dump()

    for key, value in data_to_update.items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)

    return category


async def delete_category(category: CategoryDBModel, db: AsyncSession) -> None:
    await db.delete(category)
    await db.commit()


async def verify_category_ownership(
    user_id: int, category_id: int, db: AsyncSession
) -> CategoryDBModel:
    category = await get_category_by_id_or_404(category_id=category_id, db=db)

    if category.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this category",
        )

    return category
