import os

from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine


maria_url = os.getenv("DATABASE_URL") or "mysql+pymysql://fastapi_user:fastapi_password@db:3306/fastapi_db"
engine = create_engine(maria_url)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
