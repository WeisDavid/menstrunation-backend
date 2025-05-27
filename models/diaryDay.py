from fastapi import FastAPI
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict
from typing import Optional
import datetime


class DiaryDay(SQLModel, table=True):
    __tablename__ = "diaryDay"

    id: Optional[int] = Field(default=None, primary_key=True)
    painlvl: int
    date: datetime.date
    cycleID: int
    content: str
    periodday: bool

    model_config = ConfigDict(from_attributes=True)


class DiaryDayresponse(SQLModel):
    id: int
    painlvl: int
    date: datetime.date
    content: str
    periodday: bool
    cycleID: int

    model_config = ConfigDict(from_attributes=True)