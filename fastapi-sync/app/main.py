from fastapi import FastAPI
from app.api import auth, users, tasks
from .core.logging import setup_logging

app = FastAPI()


setup_logging()


@app.get("/")
def root():
    return "API is running!"


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
