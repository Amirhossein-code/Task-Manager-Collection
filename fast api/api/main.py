from fastapi import FastAPI
from api.users import router as users_router
from api.auth import router as auth_router

app = FastAPI()

app.include_router(users_router.router)
app.include_router(auth_router.router)
