import logging
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ...models import Task, User
from ...schemas import tasks as task_schemas

logger = logging.getLogger(__name__)


def get_task_by_id(task_id: int, db: Session) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()


def get_task_by_id_or_404(task_id: int, db: Session) -> Task:
    try:
        task = get_task_by_id(task_id=task_id, db=db)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        return task
    except HTTPException as http_exc:
        raise http_exc
    except SQLAlchemyError as e:
        logger.error(
            f"Database error occurred while retrieving task with id {task_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while retrieving the task.",
        )
    except Exception as exc:
        logger.error(
            f"Unexpected error occurred while retrieving task with id {task_id}: {exc}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving the task.",
        )


def get_user_tasks(user: User, db: Session) -> List[Task]:
    try:
        tasks = db.query(Task).filter(Task.owner_id == user.id).all()
        return tasks
    except SQLAlchemyError as e:
        logger.error(
            f"Database error occurred while retrieving tasks for user with id {user.id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while retrieving user tasks.",
        )
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while retrieving tasks for user with id {user.id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving user tasks.",
        )


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
        logger.error(
            f"Database error occurred while creating a new task for user with id {user.id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the task.{e}",
        )
    except Exception as e:
        db.rollback()
        logger.error(
            f"Unexpected error occurred while creating a new task for user with id {user.id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the task. {e}",
        )


def update_task(
    task: Task,
    update_data: task_schemas.TaskUpdate,
    db: Session,
    full_update: bool = False,  # True for PUT, False for PATCH
) -> Task:
    try:
        data_to_update = update_data.model_dump(exclude_unset=not full_update)

        for key, value in data_to_update.items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(
            f"Database error occurred while updating task with id {task.id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"A database error occurred while updating the task.{e}",
        )
    except Exception as e:
        db.rollback()
        logger.error(
            f"Unexpected error occurred while updating task with id {task.id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while updating the task. {e}",
        )


def delete_task(task: Task, db: Session) -> None:
    try:
        db.delete(task)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(
            f"Database error occurred while deleting task with id {task.id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A database error occurred while deleting the task.",
        )
    except Exception as e:
        db.rollback()
        logger.error(
            f"Unexpected error occurred while deleting task with id {task.id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the task.",
        )
