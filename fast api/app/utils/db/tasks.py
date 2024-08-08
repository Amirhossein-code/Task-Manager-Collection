import logging
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...models import Task, User
from ...schemas import tasks as task_schemas

logger = logging.getLogger(__name__)


def create_new_task(
    task_data: task_schemas.TaskCreate, user: User, db: Session
) -> Task:
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        owner_id=user.id,
    )
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error.",
        )
    return new_task


def get_user_tasks_or_404(current_user: User, db: Session) -> List[task_schemas.Task]:
    try:
        tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No tasks found for the logged in user",
            )
        return tasks

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        f"Unexpected error occurred while retrieving task: {e}"

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user tasks",
        )


def get_task_by_id(task_id: int, db: Session) -> task_schemas.Task:
    return db.query(Task).filter(Task.id == task_id).first()


def get_task_by_id_or_404(task_id: int, db: Session) -> task_schemas.Task:
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        return task

    except HTTPException as http_exc:
        raise http_exc

    except Exception as exc:
        logger.error(
            f"Unexpected error occurred while retrieving task {task_id}: {exc}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


def update_task(
    task: task_schemas.Task, task_data: task_schemas.TaskUpdate, db: Session
):
    try:
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)
        return task_schemas.Task.from_orm(task)

    except Exception as e:
        logger.error(
            f"Unexpected error occurred while Updating task: {e}",
        )
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating task",
        )
