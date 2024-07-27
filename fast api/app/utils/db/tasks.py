from ...models import Task, User
from sqlalchemy.orm import Session
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
