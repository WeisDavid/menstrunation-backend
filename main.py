from typing import Annotated

from fastapi import FastAPI, Path, HTTPException, status
from fastapi.responses import  JSONResponse

from db import SessionDep, get_single_entity_by_id, create_single_entity_by_id, update_single_entity_by_id, delete_single_entity_by_id
from models.users import User, CreateUser

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/user/update/{user_id}", response_model=None)
async def update_user(user_id: Annotated[ int, Path(title="Benutzer ID", description="ID des Benutzers") ], update_request: CreateUser, session: SessionDep) -> any:
    return update_user_attributes(user_id, update_request, session)


def update_user_attributes(user_id: int, update_request: CreateUser, session: SessionDep) -> any:

    validate_update_numbers(update_request)

    update_single_entity_by_id(session, User, update_request, user_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"user_id": user_id})

def validate_update_numbers(update_request: CreateUser):

    if update_request.gewicht is not None:
        if update_request.gewicht < 0:
            raise HTTPException(400, "Übergebene Werte dürfen nicht negativ sein!")

    if update_request.groesse is not None:
        if update_request.groesse < 0:
            raise HTTPException(400, "Übergebene Werte dürfen nicht negativ sein!")

    if update_request.alter is not None:
        if update_request.alter < 0:
            raise HTTPException(400, "Übergebene Werte dürfen nicht negativ sein!")
            

@app.delete("/user_delete/{user_id}")
async def user_delete(user_id: int , session: SessionDep):

    deleted = delete_single_entity_by_id(session, User, user_id)
    if deleted is None: 
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    return JSONResponse(status_code=204, content={"message": f"User with ID {user_id} deleted successfully."})
