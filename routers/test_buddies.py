from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from db.session import get_session
from main import app

client = TestClient(app)

engine = create_engine(

    "sqlite:///testing.db", connect_args={"check_same_thread": False}
)
SQLModel.metadata.create_all(engine)

with Session(engine) as session:

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override()

    def test_get_buddies_empty():
