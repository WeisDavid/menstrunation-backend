from fastapi import FastAPI,HTTPException

from db import SessionDep, get_single_entity_by_id, create_single_entity_by_id, update_single_entity_by_id, delete_single_entity_by_id
from models.users import User, CreateUser
from pydantic import BaseModel

class userIn(BaseModel):
    username: str
    email: str
    alter: int
    gewicht: float
    groesse: float

class userOut(BaseModel):
    id: int

app = FastAPI()


@app.post("/user/", response_model=userOut)
async def create_user(user: CreateUser, session: SessionDep):
    create_single_entity_by_id(session, User, user)
    return {"id": 111}

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    if user_id == 69:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id}
