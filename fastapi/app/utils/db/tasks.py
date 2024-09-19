from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException, status

from ...models import Task as TaskDBModel
from ...models import User as UserDBModel
from ...schemas import tasks as task_schemas
from . import categories as category_crud


async def get_task_by_id(task_id: int, db: AsyncSession) -> TaskDBModel:
    stmt = select(TaskDBModel).filter(TaskDBModel.id == task_id)
    result = await db.execute(stmt)
    task = result.scalars().one_or_none()

    return task


async def get_task_by_id_or_404(task_id: int, db: AsyncSession) -> TaskDBModel:
    task = await get_task_by_id(task_id=task_id, db=db)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


async def get_user_tasks(user: UserDBModel, db: AsyncSession) -> List[TaskDBModel]:
    stmt = select(TaskDBModel).filter(TaskDBModel.owner_id == user.id)
    result = await db.execute(stmt)
    tasks = result.scalars().all()

    return tasks


async def create_new_task(
    request: task_schemas.TaskCreate, user: UserDBModel, db: AsyncSession
) -> TaskDBModel:
    category = await category_crud.get_category_by_id(request.category_id, db)

    # Check if category exits
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    # Check if the category belongs to the user
    if category.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this category"
        )

    # Create a dictionary representation of a task data (Pydantic model instance)
    task_data = request.model_dump()
    new_task = TaskDBModel(**task_data, owner_id=user.id)

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task


async def update_task(
    task: TaskDBModel,
    update_data: task_schemas.TaskUpdate,
    user: UserDBModel,
    db: AsyncSession,
    exclude_unset: bool = False,
) -> TaskDBModel:
    # Creates a dictionary representation of a task data (Pydantic model instance)
    # The exclude unset can be useful for distinguishing between PUT and PATCH request
    data_to_update = update_data.model_dump(exclude_unset=exclude_unset)

    if "category_id" in data_to_update:
        category = await category_crud.get_category_by_id(
            data_to_update["category_id"], db
        )

        # Check if category exits
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
        # Used for raising an HTTPexception for the value error that is raised
        # inside of the Task event listeners for start/finish time mismatch
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating task: {str(e)}",
        )

    return task


async def delete_task(task: TaskDBModel, db: AsyncSession) -> None:
    await db.delete(task)
    await db.commit()


async def verify_task_ownership(
    user_id: int, task_id: int, db: AsyncSession
) -> TaskDBModel:
    task = await get_task_by_id_or_404(task_id=task_id, db=db)

    if task.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task",
        )

    return task
