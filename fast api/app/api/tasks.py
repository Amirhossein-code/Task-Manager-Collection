from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..dependencies.current_user import get_current_user_db_dependency
from ..models import Task, User
from ..schemas import tasks as task_schemas
from ..utils.db import tasks as task_crud

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/", response_model=task_schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: task_schemas.TaskCreate,
    current_user: User = Depends(get_current_user_db_dependency),
    db: Session = Depends(get_db),
):
    new_task = task_crud.create_new_task(
        task_data=task,
        current_user=current_user,
        db=db,
    )
    return new_task


@router.get(
    "/me", response_model=List[task_schemas.Task], status_code=status.HTTP_200_OK
)
def get_users_tasks(
    current_user: User = Depends(get_current_user_db_dependency),
    db: Session = Depends(get_db),
):
    tasks = task_crud.get_user_tasks(
        current_user=current_user,
        db=db,
    )
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return tasks


@router.get("/{task_id}")
def get_task(
    task_id: int,
    user: User = Depends(get_current_user_db_dependency),
    db: Session = Depends(get_db),
):
    task = task_crud.get_task_by_id_or_404(task_id=task_id, db=db)
    if task.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )
    return task


# {
#   "full_name": "string",
#   "email": "user2@example.com",
#   "password": "Hello123@World"
# }
