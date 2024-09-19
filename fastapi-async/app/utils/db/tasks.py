from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...models import Task, User
from ...schemas import tasks as task_schemas
from . import categories as category_crud


async def get_task_by_id(task_id: int, db: AsyncSession) -> Task:
    stmt = select(Task).filter(Task.id == task_id)
    result = await db.execute(stmt)
    task = result.scalars().one_or_none()
    return task


async def get_task_by_id_or_404(task_id: int, db: AsyncSession) -> Task:
    task = await get_task_by_id(task_id=task_id, db=db)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


async def get_user_tasks(user: User, db: AsyncSession) -> List[Task]:
    stmt = select(Task).filter(Task.owner_id == user.id)
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def create_new_task(
    request: task_schemas.TaskCreate, user: User, db: AsyncSession
) -> Task:
    category = await category_crud.get_category_by_id(request.category_id, db)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    # Check if the category belongs to the user
    if category.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this category"
        )

    task_data = request.model_dump()
    new_task = Task(**task_data, owner_id=user.id)

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def update_task(
    task: Task,
    update_data: task_schemas.TaskUpdate,
    user: User,
    db: AsyncSession,
    full_update: bool = False,  # True for PUT, False for PATCH
) -> Task:
    data_to_update = update_data.model_dump(exclude_unset=not full_update)

    if "category_id" in data_to_update:
        category = await category_crud.get_category_by_id(
            data_to_update["category_id"], db
        )

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )

        # Check if the category belongs to the user
        if category.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not own this category",
            )

    for key, value in data_to_update.items():
        setattr(task, key, value)
    try:
        # This line triggers event listener so the exception is handled correctly
        await db.flush()

        await db.commit()
        await db.refresh(task)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating task: {str(e)}",
        )
    return task


async def delete_task(task: Task, db: AsyncSession) -> None:
    await db.delete(task)
    await db.commit()
