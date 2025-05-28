from sqlmodel import Field, SQLModel
from pydantic import ConfigDict

class Product(SQLModel, table=True):
    __tablename__ = "products"
    id: int  = Field(primary_key=True)
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class Productresponse(SQLModel):
    id: int
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

