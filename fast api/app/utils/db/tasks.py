from typing import List

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
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_user_tasks(current_user: User, db: Session) -> List[Task]:
    return db.query(Task).filter(Task.owner_id == current_user.id).all()
