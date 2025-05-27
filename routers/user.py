from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi.responses import JSONResponse
from typing import Annotated

from db.default import SessionDep
from models.user import UserRequest, CreateUser, UserInDB
from db.users import get_single_user_by_id, create_user_in_db, update_user_in_db, delete_user_in_db
from utils.token import get_current_user


router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@router.get("/get/{user_id}")
def get_user(
    user_id: Annotated[
        int,
        Depends(get_current_user)
    ],
    session: SessionDep,
) -> UserInDB:
    response = get_single_user_by_id(session, UserRequest, user_id)
    if response is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    return response


@router.post("/create")
def create_user(
    user: CreateUser,
    session: SessionDep
):
    created_user = create_user_in_db(session, user)
    if created_user is None:
        raise HTTPException(status_code=400, detail="Invalid user data")
    return created_user


@router.put("/update/{user_id}", response_model=None)
def update_user(
    user_id: Annotated[
        int,
        Path(title="Benutzer ID", description="ID des Benutzers")
    ],
    update_request: CreateUser,
    session: SessionDep
) -> any:
    return update_user_in_db(session, UserRequest, update_request, user_id)
            

@router.delete("/delete/{user_id}")
def user_delete(
    user_id: int,
    session: SessionDep
):
    deleted = delete_user_in_db(session, UserRequest, user_id)
    if deleted is None: 
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    return JSONResponse(status_code=204, content={"message": f"User with ID {user_id} deleted successfully."})
