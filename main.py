from fastapi import FastAPI

from db import SessionDep, get_single_entity_by_id, create_single_entity_by_id, update_single_entity_by_id, delete_single_entity_by_id
from models.users import User, CreateUser

app = FastAPI()



@app.get("/user_delete/{user_id}")
async def user_delete(user_id: int):
    if user exists:    
        delete = {"delete_message": "User deleted successfully"}
        return delete_message 
    else:
        return {"User does not exist"}