from sqlmodel import Field, SQLModel
from pydantic import ConfigDict


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    """email: str
    password: str"""
    alter: int
    gewicht: float
    groesse: float


class CreateUser(SQLModel):
    username: str
    """email: str
    password: str"""
    alter: int
    gewicht: float
    groesse: float

    model_config = ConfigDict(from_attributes=True)