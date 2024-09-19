from contextlib import asynccontextmanager

import uvicorn

from app.api import auth, categories, tasks, users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.database import sessionmanager
from .core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title="Task manager")


setup_logging()


@app.get("/")
async def root():
    return "API is running!"


@app.get("/health")
async def health():
    # Health Check endpoint
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(categories.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
