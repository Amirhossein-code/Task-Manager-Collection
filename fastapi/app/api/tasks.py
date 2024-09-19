from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db_session
from ..dependencies import get_current_active_user_db_dependency
from ..schemas import tasks as task_schemas, users as user_schemas
from ..utils.db import tasks as task_crud

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/", response_model=task_schemas.Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: task_schemas.TaskCreate,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: AsyncSession = Depends(get_db_session),
):
    new_task = await task_crud.create_new_task(
        request=request,
        user=user,
        db=db,
    )
    return new_task


@router.get("/", response_model=List[task_schemas.Task], status_code=status.HTTP_200_OK)
async def get_users_tasks(
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: AsyncSession = Depends(get_db_session),
):
    tasks = await task_crud.get_user_tasks(
        user=user,
        db=db,
    )
    return tasks


@router.get(
    "/{task_id}", response_model=task_schemas.Task, status_code=status.HTTP_200_OK
)
async def get_task_by_id(
    task_id: int,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: AsyncSession = (Depends(get_db_session)),
):
    task = await task_crud.get_task_by_id_or_404(task_id=task_id, db=db)

    if task.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )

    return task


@router.put(
    "/{task_id}", response_model=task_schemas.Task, status_code=status.HTTP_200_OK
)
async def put_update_task(
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    task_id: int,
    update_task_data: task_schemas.TaskUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    task = await task_crud.get_task_by_id_or_404(task_id=task_id, db=db)

    if task.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task",
        )

    updated_task = await task_crud.update_task(
        task=task,
        update_data=update_task_data,
        db=db,
        full_update=True,
    )

    return updated_task


@router.patch(
    "/{task_id}",
    response_model=task_schemas.Task,
    status_code=status.HTTP_200_OK,
)
async def patch_update_task(
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    task_id: int,
    update_task_data: task_schemas.TaskUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    task = await task_crud.get_task_by_id_or_404(task_id, db)

    if task.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to Update this task",
        )

    updated_task = await task_crud.update_task(
        task=task, update_data=update_task_data, db=db, full_update=False
    )

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    task_id: int,
    db: AsyncSession = Depends(get_db_session),
):
    task = await task_crud.get_task_by_id_or_404(task_id=task_id, db=db)

    if task.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task",
        )

    await task_crud.delete_task(task=task, db=db)

    return None
