from fastapi import FastAPI
from api.auth.router import auth as auth_router, users as users_router

app = FastAPI()

app.include_router(users_router.router)
app.include_router(auth_router.router)
