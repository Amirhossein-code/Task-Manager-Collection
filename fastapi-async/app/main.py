from fastapi import FastAPI

from app.api import auth, tasks, users

from .core.logging import setup_logging

from contextlib import asynccontextmanager

import uvicorn
from core.database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title="Task manager", docs_url="/api/docs")


setup_logging()


@app.get("/")
async def root():
    return "API is running!"


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
