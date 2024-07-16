from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/auth/token")
def get_token():
    pass
