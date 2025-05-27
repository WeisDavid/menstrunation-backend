from fastapi import Depends, FastAPI, HTTPException, Query, APIRouter
from pydantic import BaseModel
from models.diaryDay import DiaryDay, DiaryDayresponse
from db import SessionDep

router = APIRouter(
    prefix="/diaryDay",
    tags=["diaryDay"],
)


@router.get("/{id}")
async def get_diaryDay(id: int, session: SessionDep):
    DiaryDay = session.get(DiaryDay, id)
    if DiaryDay is None:
        raise HTTPException(status_code=404, detail="Diary entry not found")

    return DiaryDayresponse.model_validate(DiaryDay)