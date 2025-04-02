from fastapi import FastAPI

app = FastAPI()

testUser = {
    "id": "55",
    "userName": "testman",
    "pw": "wawa123",
    "email": "testmail@test.com",
    "alter": 22,
    "gewicht": 80,
    "größe": 181
}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/user/getById/{user_id}")
async def get_user_by_id(user_id: str):
    if user_id == "55":
        return testUser
    else:
        return {"message": "User with ID " + user_id + " does not exist!"}


