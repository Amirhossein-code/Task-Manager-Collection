from typing import Annotated, List

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

from ..core.database import get_db_session
from ..dependencies import get_current_active_user_db_dependency
from ..schemas import tasks as task_schemas
from ..schemas import users as user_schemas
from ..utils.db import tasks as task_crud

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/", response_model=List[task_schemas.Task], status_code=status.HTTP_200_OK)
async def get_users_tasks(
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    tasks = await task_crud.get_user_tasks(user=user, db=db)

    return tasks


@router.get(
    "/{task_id}", response_model=task_schemas.Task, status_code=status.HTTP_200_OK
)
async def get_task_by_id(
    task_id: int,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    task = await task_crud.verify_task_ownership(
        user_id=user.id, task_id=task_id, db=db
    )

    return task


@router.post("/", response_model=task_schemas.Task, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    request: task_schemas.TaskCreate,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    new_task = await task_crud.create_new_task(
        request=request,
        user=user,
        db=db,
    )

    return new_task


@router.put(
    "/{task_id}", response_model=task_schemas.Task, status_code=status.HTTP_200_OK
)
async def put_update_task(
    task_id: int,
    request: task_schemas.TaskUpdate,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    task = await task_crud.verify_task_ownership(
        user_id=user.id, task_id=task_id, db=db
    )

    updated_task = await task_crud.update_task(
        task=task,
        update_data=request,
        user=user,
        db=db,
        exclude_unset=False,
    )

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user: Annotated[
        user_schemas.UserDisplay, Depends(get_current_active_user_db_dependency)
    ],
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    task = await task_crud.verify_task_ownership(
        user_id=user.id, task_id=task_id, db=db
    )

    await task_crud.delete_task(task=task, db=db)

    return None
