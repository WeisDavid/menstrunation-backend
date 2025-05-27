from fastapi import APIRouter
from typing import Annotated


from db.default import SessionDep
from fastapi import Path, HTTPException
from fastapi.responses import  JSONResponse

from db.buddies import create_buddy_in_db, delete_buddies_by_id
from models.buddy import BuddyCreate

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