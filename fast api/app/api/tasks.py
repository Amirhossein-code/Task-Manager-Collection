from typing import List

from fastapi import APIRouter, Depends, status
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


@router.get("/", response_model=List[task_schemas.Task], status_code=status.HTTP_200_OK)
def get_users_tasks(
    current_user: User = Depends(get_current_user_db_dependency),
    db: Session = Depends(get_db),
):
    tasks = task_crud.get_user_tasks(
        current_user=current_user,
        db=db,
    )
    return tasks


# {
#   "full_name": "string",
#   "email": "user2@example.com",
#   "password": "Hello123@World"
# }
