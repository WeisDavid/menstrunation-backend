import pytest
from fastapi.testclient import TestClient
from db.session import get_session
from models.buddy import BuddyTable
from utils.token import get_current_user
from utils.pw_auth import get_password_hash
from sqlmodel import create_engine, SQLModel, Session, select
from sqlmodel.pool import StaticPool

from main import app
from models.user import UserTable


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    def get_current_user_override():
        return UserTable(id=1, username="test", email="test@mail.com")

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_buddy_success(session: Session, client: TestClient):
    user_other = UserTable(id= 2, username="test2", email="test2@mail.com", hashed_password="pass2")

    session.add(user_other)
    session.commit()

    response = client.post("/buddy/create", json={ "username": "test2" })
    data = response.json()

    assert response.status_code == 204
    assert "test2" in data["message"]

    buddies = session.exec(select(BuddyTable)).all()
    assert len(buddies) == 1
    buddy = buddies[0]
    assert buddy.userID1 == 1
    assert buddy.userID2 == user_other.id

def test_create_buddy_failure_not_found(session: Session, client: TestClient):
    response = client.post("/buddy/create", json={"username": "test2"})
    data = response.json()

    assert response.status_code == 404
    assert "not found" in data["detail"]

def test_delete_buddy_success_buddy_by_me(session: Session, client: TestClient):
    user_other = UserTable(id=2, username="test2", email="test2@mail.com", hashed_password="pass2")
    buddy_by_me = BuddyTable(userID1=1, userID2=2)

    session.add(user_other)
    session.add(buddy_by_me)
    session.commit()

    response = client.request("DELETE","/buddy/delete", json={ "username": "test2" })
    data = response.json()

    assert response.status_code == 204
    assert "test2" in data["message"]

    buddies = session.exec(select(BuddyTable)).all()
    assert len(buddies) == 0

def test_delete_buddy_success_buddy_by_other(session: Session, client: TestClient):
    user_other = UserTable(id=2, username="test2", email="test2@mail.com", hashed_password="pass2")
    buddy_by_me = BuddyTable(userID1=2, userID2=1)

    session.add(user_other)
    session.add(buddy_by_me)
    session.commit()

    response = client.request("DELETE", "/buddy/delete", json={"username": "test2"})
    data = response.json()

    assert response.status_code == 204
    assert "test2" in data["message"]

    buddies = session.exec(select(BuddyTable)).all()
    assert len(buddies) == 0

def test_delete_buddy_failure_user_not_found(session: Session, client: TestClient):
    response = client.request("DELETE", "/buddy/delete", json={"username": "test2"})
    data = response.json()

    assert response.status_code == 404
    assert "not found" in data["detail"]

def test_delete_buddy_failure_no_buddies(session: Session, client: TestClient):
    user_other = UserTable(id=2, username="test2", email="test2@mail.com", hashed_password="pass2")

    session.add(user_other)
    session.commit()


    response = client.request("DELETE", "/buddy/delete", json={"username": "test2"})
    data = response.json()

    assert response.status_code == 404
    assert "not found" in data["detail"]

def test_delete_buddy_failure_no_buddies_with_specified_user(session: Session, client: TestClient):
    user_other = UserTable(id=2, username="test2", email="test2@mail.com", hashed_password="pass2")
    buddy_by_me = BuddyTable(userID1=1, userID2=4)

    session.add(user_other)
    session.add(buddy_by_me)
    session.commit()

    response = client.request("DELETE", "/buddy/delete", json={"username": "test2"})
    data = response.json()

    assert response.status_code == 404
    assert "not found" in data["detail"]

