from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String
from pydantic import ConfigDict

from utils.pw_auth import get_password_hash


class UserBase(SQLModel):
    username: str
    email: str
    age: int | None
    weight: float | None
    height: float | None


class UserRequest(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

class CreateUser(UserBase):
    password: str

    model_config = ConfigDict(from_attributes=True)

class UpdateUser(UserBase):
    model_config = ConfigDict(from_attributes=True)

class UserInDB(UserBase):
    id: int
    hashed_password: str = Field(
        sa_column=Column("password", String)
    )

    model_config = ConfigDict(from_attributes=True)

    
class UserTable(UserInDB, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_create_user(cls, user: CreateUser):
        """
        Create a UserInDB from a CreateUser.
        
        Exclude the `password` field from the `CreateUser` and add a `hashed_password`
        field with the hashed password.
        
        Args:
        - user (CreateUser): The CreateUser instance to convert.
        
        Returns:
        - UserInDB: The converted UserInDB instance.
        """
        return cls(
            **user.model_dump(exclude={"password"}),
            hashed_password=get_password_hash(user.password)
        )