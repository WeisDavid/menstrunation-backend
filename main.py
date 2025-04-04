from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr

from db import SessionDep, get_single_entity_by_id, create_single_entity_by_id, update_single_entity_by_id, delete_single_entity_by_id
from models.users import User, CreateUser

app = FastAPI()

class UserModell(BaseModel):
    id: int
    pw: str
    email: EmailStr
    alter: int | None
    gewicht: float | None
    größe: float | None

class UpdateRequest(BaseModel):
    username: str | None = Field( default=None, title="Neuer Benutzername" )
    pw: str | None = Field( default=None, title="Neues Passwort der Benutzers" )
    email: EmailStr | None = Field( default=None, title="Neues Email des Benutzers" )
    alter: int | None = Field( default=None, title="Neues Alter des Benutzers" )
    gewicht: float | None = Field( default=None, title="Neues Gewicht des Benutzers" )
    größe: float | None = Field( default=None, title="Neue Größe des Benutzers" )

user_list: list[UserModell] = []



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/user/update/{user_id}")
async def update_user(user_id: Annotated[ int, Query(title="Benutzer ID", description="ID des Benutzers") ], update_request: UpdateRequest):
    return 1
