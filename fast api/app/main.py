from fastapi import FastAPI
from app.api import auth, users, tasks

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

#ssfdafsdfsd@example.com
#ILove@FastAPI3