from markdown_it.rules_block import table
from pydantic import ConfigDict, BaseModel
from sqlmodel import SQLModel, Field


class BuddyBase(SQLModel):
    userID1: int | None = Field(default=None, foreign_key="users.id", ondelete="CASCADE")
    userID2: int | None = Field(default=None, foreign_key="users.id", ondelete="CASCADE")


class BuddyFrontend(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)

class BuddyInDB(BuddyBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BuddyTable(BuddyInDB, table=True):
    __tablename__ = "buddies"

    id: int | None = Field(default=None, primary_key=True)
