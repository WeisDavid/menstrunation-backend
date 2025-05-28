from fastapi import FastAPI
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict
from typing import Optional
import datetime


class DiaryDay(SQLModel, table=True):
    __tablename__ = "diaryDays"

    id: int = Field (primary_key=True)
    painlvl: int
    date: datetime.date
    content: str
    isPeriod: bool

    model_config = ConfigDict(from_attributes=True)


class DiaryDayresponse(SQLModel):
    id: int
    painlvl: int
    date: datetime.date
    content: str
    isPeriod: bool

    model_config = ConfigDict(from_attributes=True)