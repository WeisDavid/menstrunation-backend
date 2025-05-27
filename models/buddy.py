from markdown_it.rules_block import table
from pydantic import ConfigDict
from sqlmodel import SQLModel, Field


class BuddyBase(SQLModel):
    benutzer_id_1: int | None = Field(default=None, foreign_key="user.id")
    benutzer_id_2: int | None = Field(default=None, foreign_key="user.id")


class BuddyCreate(BuddyBase):
    model_config = ConfigDict(from_attributes=True)

class BuddyInDB(BuddyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BuddyTable(BuddyInDB, table=True):
    __tablename__ = "buddies"

    id: int | None = Field(default=None, primary_key=True)
