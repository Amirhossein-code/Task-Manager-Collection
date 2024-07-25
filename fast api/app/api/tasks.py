from fastapi import APIRouter, status

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task():
    pass
