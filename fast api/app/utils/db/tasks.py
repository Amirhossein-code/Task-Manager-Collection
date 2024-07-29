from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...models import Task, User
from ...schemas import tasks as task_schemas


def create_new_task(
    task_data: task_schemas.TaskCreate, current_user: User, db: Session
) -> Task:
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        owner_id=current_user.id,
    )
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error.")
    return new_task


def get_user_tasks(current_user: User, db: Session) -> List[task_schemas.Task]:
    try:
        return db.query(Task).filter(Task.owner_id == current_user.id).all()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user tasks",
        )


def get_task_by_id(task_id: int, db: Session) -> task_schemas.Task:
    try:
        return db.query(Task).filter(Task.id == task_id).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving tasks by id",
        )


def get_task_by_id_or_404(task_id: int, db: Session) -> task_schemas.Task:
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving tasks by id",
        )
