from fastapi import FastAPI

from routers.user import router as user_router
from routers.buddies import buddy_router


app = FastAPI()
app.include_router(user_router)
app.include_router(buddy_router)
