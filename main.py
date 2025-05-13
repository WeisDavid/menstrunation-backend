from fastapi import FastAPI

app = FastAPI()



@app.get("/user_delete/{user_id}")
async def user_delete(user_id: int):
    if (user_id not NULL):    
        delete = {"delete_message": "User deleted successfully"}
        return delete_message 
    else:
        return {"User does not exist"}