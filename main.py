from fastapi import FastAPI

from routers.user import router as user_router
from routers.token import router as token_router


app = FastAPI()
app.include_router(user_router)
app.include_router(token_router)
