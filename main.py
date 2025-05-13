from typing import Annotated

from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field, EmailStr

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
    email: EmailStr | None = Field( default=None, title="Neue Email des Benutzers" )
    alter: int | None = Field( default=None, title="Neues Alter des Benutzers" )
    gewicht: float | None = Field( default=None, title="Neues Gewicht des Benutzers" )
    größe: float | None = Field( default=None, title="Neue Größe des Benutzers" )

class UpdateResponse(BaseModel):
    user_id: int = Field(title="ID des Benutzers")
    status_code: int = Field(default=200, title="HTTP Statuscode der Response")

user_list = {
    1: {
        "username": "theWoman",
        "pw": "lolala",
        "email": "woman@mail.com",
        "alter": 22,
        "gewicht": 67.8,
        "größe": 175.0
    },
    4: {
        "username": "Beth",
        "pw": "thissucks",
        "email": "bethymay@mail.com",
        "alter": 18,
        "gewicht": 72.0,
        "größe": 168.0
    },
    5: {
        "username": "Markus",
        "pw": "leckdieAier",
        "email": "ruxman@mail.com",
        "alter": 20,
        "gewicht": 99.0,
        "größe": 178.0
    }
}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/user/update/{user_id}", response_model=UpdateResponse)
async def update_user(user_id: Annotated[ int, Path(title="Benutzer ID", description="ID des Benutzers") ], update_request: UpdateRequest) -> any:
    return update_user_attributes(user_id, update_request)


def update_user_attributes(user_id: int, update_request: UpdateRequest) -> any:

    validate_update_numbers(update_request)

    if user_id not in user_list:
        not_found_message = f"Der User mit der ID {user_id} existiert nicht!"
        raise HTTPException(404, not_found_message)

    existing_user = user_list.get(user_id)

    if update_request.größe is not None:
        existing_user.update({"größe": update_request.größe})

    if update_request.alter is not None:
        existing_user.update({"alter": update_request.alter})

    if update_request.gewicht is not None:
        existing_user.update({"gewicht": update_request.gewicht})

    if update_request.pw is not None:
        existing_user.update({"pw": update_request.pw})

    if update_request.username is not None:
        existing_user.update({"username": update_request.username})

    if update_request.email is not None:
        existing_user.update({"email": update_request.email})

    user_list.update({user_id: existing_user})

    successful_response = {
        "user_id": user_id,
        "status_code": 200
    }

    return successful_response

def validate_update_numbers(update_request: UpdateRequest):

    if update_request.gewicht is not None:
        if update_request.gewicht < 0:
            raise HTTPException(400, "Übergebene Werte dürfen nicht negativ sein!")

    if update_request.größe is not None:
        if update_request.größe < 0:
            raise HTTPException(400, "Übergebene Werte dürfen nicht negativ sein!")

    if update_request.alter is not None:
        if update_request.alter < 0:
            raise HTTPException(400, "Übergebene Werte dürfen nicht negativ sein!")
