from fastapi import FastAPI

class userIn:
    username: str
    email: str
    alter: int
    gewicht: float
    groesse: float

class userOut:
    id: int

app = FastAPI()


@app.get("/")
async def root():
    
    return {"message": "Hello World"}


@app.get("/Philipp/")
async def get_user(user_id):
    id = 69
    username = "Philipp"
    email = "Philipp@KING.com"
    alter = 69
    gewicht = 69.69
    groesse = 69.69 
    return {  "id": id, "username": username, "email":email, "alter":alter, "gewicht":gewicht, "groesse":groesse}

@app.post("/user/", response_model=userOut)
async def create_user(user: userIn):
    return user