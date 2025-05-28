from fastapi import APIRouter, Depends
from typing import Annotated


from db.session import SessionDep
from fastapi import Path, HTTPException
from fastapi.responses import  JSONResponse

from db.buddies import create_buddy_in_db, delete_buddies_by_id, get_buddies_by_id
from models.buddy import BuddyCreate
from models.user import UserResponse, UserInDB
from utils.token import get_current_user

buddy_router = APIRouter(
    prefix="/buddy",
    tags=["Buddy"],
)

@buddy_router.post("/create", response_model=None)
async def create_buddy(buddy: BuddyCreate, session: SessionDep) -> any:
    created_buddy_id = create_buddy_in_db(session, buddy)
    if created_buddy_id is None:
        raise HTTPException(status_code=400, detail="Invalid Buddy Data")

    return JSONResponse(status_code=200, content={"buddy_id": created_buddy_id})

@buddy_router.delete("/{buddy_id}/delete", response_model=None)
async def delete_buddy(buddy_id: Annotated[int, Path(title="Buddy ID", description="ID der Freundschaft")], session: SessionDep):
    deleted = delete_buddies_by_id(session, buddy_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail=f"Buddy with ID {buddy_id} not found")

    return JSONResponse(status_code=204, content={"message": f"Buddy with ID {buddy_id} deleted successfully"})

@buddy_router.get("/get", response_model=list[UserResponse])
async def get_my_buddies(current_user: Annotated[UserInDB, Depends(get_current_user)], session: SessionDep):
    my_buddies = get_buddies_by_id(session, current_user.id)
    if not my_buddies:
        return []

    return [UserResponse.model_validate(user) for user in my_buddies]