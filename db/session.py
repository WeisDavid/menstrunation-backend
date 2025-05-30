import os

from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine


maria_url = os.getenv("DATABASE_URL") or "mysql+pymysql://fastapi_user:fastapi_password@db:3306/fastapi_db"
engine = create_engine(maria_url)

def get_session():
    """
    Yields a database session.

    The session is created using the engine connected to the database URL
    specified in the environment variable `DATABASE_URL`. If `DATABASE_URL` is
    not set, the session is created using the default database URL.

    The session is automatically closed when the context manager is exited.

    Returns:
        Session: The database session.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
