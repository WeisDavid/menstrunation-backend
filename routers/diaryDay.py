from fastapi import HTTPException, APIRouter
from fastapi.responses import  JSONResponse
from models.diaryDay import DiaryDay, DiaryDayresponse, DiaryDayinput
from db.session import SessionDep

router = APIRouter(
    prefix="/diaryDay",
    tags=["diaryDay"],
)


@router.get("/{id}")
async def get_diaryDay(id: int, session: SessionDep):
    diaryDay = session.get(DiaryDay, id)
    if diaryDay is None:
        raise HTTPException(status_code=404, detail="Diary entry not found")

    return DiaryDayresponse.model_validate(diaryDay)



@router.delete("/{id}")
async def delete_diaryDay(id: int, session: SessionDep):
    diaryday = session.get(DiaryDay, id)
    if not diaryday:
        raise HTTPException(status_code=404, detail=f"Diary entry with ID {id} not found")
    session.delete(diaryday)
    session.commit()
    
    return JSONResponse(status_code=204, content={"message": f"User with ID {id} deleted successfully."})

#@router.post("/diaryDay/", response_model=DiaryDayresponse)
#async def create_diaryDay(diaryDay: DiaryDayinput, session: SessionDep):
#    diaryDay_table = DiaryDay.model_validate(diaryDay)
 
#    session.add(diaryDay_table)
#    session.commit()
#    session.refresh(diaryDay_table)
 
#    return DiaryDayresponse.model_validate(diaryDay_table)

@router.post("/diaryDay/", response_model=DiaryDayresponse)
async def create_diaryDay(diaryDay: DiaryDayinput, session: SessionDep):
    user_table = DiaryDay(**diaryDay.model_dump())  # KEIN model_validate

    session.add(user_table)
    session.commit()
    session.refresh(user_table)

    return DiaryDayresponse.model_validate(user_table)