from fastapi import FastAPI

app = FastAPI()



@app.get("/user_delete/{user_id}")
async def user_delete(user_id: int):

    user_exists = True
    # in der wahren anwendung muss hier noch eine DB-Abfrage stattfinden, ob der User existiert mittels einer query

    if user_exists:
        delete_message = "User deleted successfully"    
        return delete_message 
    else:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")