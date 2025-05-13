from fastapi import FastAPI

app = FastAPI()



@app.get("/user_delete/{user_id}")
async def user_delete(user_id: int):    
    delete = {"delete_message": "User deleted successfully"}
    return delete
