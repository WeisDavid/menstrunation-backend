from fastapi import FastAPI

from routers.user import router as user_router
from routers.buddies import buddy_router

from db import SessionDep, get_single_entity_by_id, create_single_entity_by_id, update_single_entity_by_id, delete_single_entity_by_id
from models.users import User, CreateUser
from pydantic import BaseModel

from routers.products import router as products_router
from routers.diaryDay import router as diaryDay_router


app = FastAPI()
app.include_router(diaryDay_router)
app.include_router(user_router)
app.include_router(buddy_router)
