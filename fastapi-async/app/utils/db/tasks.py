from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...models import Task, User
from ...schemas import tasks as task_schemas


async def get_task_by_id(task_id: int, db: AsyncSession) -> Task:
    user = await db.query(Task).filter(Task.id == task_id).first()
    return user


async def get_task_by_id_or_404(task_id: int, db: AsyncSession) -> Task:
    task = await get_task_by_id(task_id=task_id, db=db)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


async def get_user_tasks(user: User, db: AsyncSession) -> List[Task]:
    tasks = await db.query(Task).filter(Task.owner_id == user.id).all()
    return tasks


async def create_new_task(
    request: task_schemas.TaskCreate, user: User, db: AsyncSession
) -> Task:
    task_data = request.model_dump()
    new_task = Task(**task_data, owner_id=user.id)

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def update_task(
    task: Task,
    update_data: task_schemas.TaskUpdate,
    db: AsyncSession,
    full_update: bool = False,  # True for PUT, False for PATCH
) -> Task:
    data_to_update = update_data.model_dump(exclude_unset=not full_update)

    for key, value in data_to_update.items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(task: Task, db: AsyncSession) -> None:
    await db.delete(task)
    await db.commit()
