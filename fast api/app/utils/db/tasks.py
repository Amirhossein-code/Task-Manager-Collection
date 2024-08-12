import logging
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ...models import Task, User
from ...schemas import tasks as task_schemas

logger = logging.getLogger(__name__)


def create_new_task(request: task_schemas.TaskCreate, user: User, db: Session) -> Task:
    try:
        task_data = request.model_dump()
        new_task = Task(**task_data, owner_id=user.id)

        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task.",
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
    # return new_task


def get_user_tasks_or_404(user: User, db: Session) -> List[Task]:
    try:
        tasks = db.query(Task).filter(Task.owner_id == user.id).all()
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


def get_task_by_id(task_id: int, db: Session) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()


def get_task_by_id_or_404(task_id: int, db: Session) -> Task:
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


def update_task(task: Task, request: task_schemas.TaskUpdate, db: Session) -> Task:
    try:
        for key, value in request.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)
        return task

    except Exception as e:
        logger.error(
            f"Unexpected error occurred while Updating task: {e}",
        )
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating task",
        )


def delete_task(task: Task, db: Session) -> None:
    db.delete(task)
    db.commit()


def patch_task(
    task: Task,
    update_task_data: task_schemas.TaskUpdate,
    db: Session,
) -> Task:
    for key, value in update_task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
