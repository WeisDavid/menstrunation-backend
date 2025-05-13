from fastapi import FastAPI, HTTPException

from db import SessionDep, get_single_entity_by_id, create_single_entity_by_id, update_single_entity_by_id, delete_single_entity_by_id
from models.users import User, CreateUser

app = FastAPI()



@app.get("/user_delete/{user_id}")
async def user_delete(user_id: int , session: SessionDep):

    deleted = delete_single_entity_by_id(session, User, user_id)
    if deleted is None: 
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    return JSONResponse(status_code=204, content={"message": f"User with ID {user_id} deleted successfully."})