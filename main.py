from fastapi import FastAPI

from db import SessionDep, get_single_entity_by_id, create_single_entity_by_id, update_single_entity_by_id, delete_single_entity_by_id
from models.users import User, CreateUser

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
