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

@app.get("/user/getById/{userId}")
async def getUserById(userId: str):
    if userId == "55":
        return testUser
    else:
        return {"message": "User with ID " + userId + " does not exist!"}


