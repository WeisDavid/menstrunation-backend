from fastapi import FastAPI

from routers.user import router as user_router
from routers.buddies import buddy_router
from routers.diaryDay import router as diaryDay_router


app = FastAPI()
app.include_router(diaryDay_router)
app.include_router(user_router)
app.include_router(buddy_router)
