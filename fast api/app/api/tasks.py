from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas import tasks as task_schemas
from ..models import User, Task
from ..dependencies.current_user import get_current_user_db_dependency

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
    # Create a new task instance
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        owner_id=current_user.id,
    )
    # Add and commit the new task to the database
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
