from fastapi import FastAPI
from api.core.router import auth as auth_router, users as users_router
from api.tasks.router import router as tasks_router

app = FastAPI()

app.include_router(users_router.router)
app.include_router(auth_router.router)
app.include_router(tasks_router.router)
