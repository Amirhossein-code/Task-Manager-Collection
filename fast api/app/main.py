from fastapi import FastAPI
from . import schemas

app = FastAPI()


@app.post("/task")
def create_task(request: schemas.Task):
    return request
