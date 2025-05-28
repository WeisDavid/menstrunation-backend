# tests/test_user_db.py

import pytest
from unittest.mock import MagicMock
from src.models.user import UserTable, UserInDB, CreateUser, UpdateUser
from src.db.users import (
    get_all_users_in_db,
    get_single_user_by_id,
    get_single_user_by_username,
    create_user_in_db,
    update_user_in_db,
    delete_user_in_db,
)


def test_get_all_users_in_db():
    user1 = UserTable(id=1, username="user1", email="u1@example.com")
    user2 = UserTable(id=2, username="user2", email="u2@example.com")

    session = MagicMock()
    session.exec.return_value.all.return_value = [user1, user2]

    result = get_all_users_in_db(session)

    assert len(result) == 2
    assert result[0].username == "user1"
    assert session.exec.called


def test_get_single_user_by_id_found():
    user = UserTable(id=1, username="user", email="user@example.com")
    session = MagicMock()
    session.get.return_value = user

    result = get_single_user_by_id(session, 1)

    assert isinstance(result, UserInDB)
    assert result.username == "user"
    session.get.assert_called_once_with(UserTable, 1)


def test_get_single_user_by_id_not_found():
    session = MagicMock()
    session.get.return_value = None

    result = get_single_user_by_id(session, 999)

    assert result is None
    session.get.assert_called_once()


def test_get_single_user_by_username_found():
    user = UserTable(id=1, username="test", email="t@example.com")

    session = MagicMock()
    session.exec.return_value.first.return_value = user

    result = get_single_user_by_username(session, "test")

    assert isinstance(result, UserInDB)
    assert result.username == "test"
    session.exec.assert_called_once()


def test_get_single_user_by_username_not_found():
    session = MagicMock()
    session.exec.return_value.first.return_value = None

    result = get_single_user_by_username(session, "nonexistent")

    assert result is None
    session.exec.assert_called_once()


def test_create_user_in_db(monkeypatch):
    user_data = CreateUser(username="new", email="new@example.com")
    user_model = UserTable(id=1, username="new", email="new@example.com")

    session = MagicMock()

    monkeypatch.setattr(UserTable, "from_create_user", lambda _: user_model)

    result = create_user_in_db(session, user_data)

    assert isinstance(result, UserInDB)
    assert result.username == "new"
    session.add.assert_called_once_with(user_model)
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(user_model)


def test_update_user_in_db_found(monkeypatch):
    user_model = UserTable(id=1, username="before", email="before@example.com")
    updated_data = UpdateUser(email="after@example.com")

    session = MagicMock()
    session.get.return_value = user_model

    # Patch model_dump and sqlmodel_update
    monkeypatch.setattr(updated_data, "model_dump", lambda **kwargs: {"email": "after@example.com"})
    monkeypatch.setattr(user_model, "sqlmodel_update", lambda data: user_model.__setattr__("email", data["email"]))

    result = update_user_in_db(session, updated_data, user_id=1)

    assert isinstance(result, UserInDB)
    assert result.email == "after@example.com"
    session.commit.assert_called_once()


def test_update_user_in_db_not_found():
    session = MagicMock()
    session.get.return_value = None

    updated_data = UpdateUser(email="doesntmatter@example.com")
    result = update_user_in_db(session, updated_data, 999)

    assert result is None
    session.get.assert_called_once()


def test_delete_user_in_db_found():
    user = UserTable(id=1, username="delete", email="d@example.com")
    session = MagicMock()
    session.get.return_value = user

    result = delete_user_in_db(session, 1)

    assert result == 1
    session.delete.assert_called_once_with(user)
    session.commit.assert_called_once()


def test_delete_user_in_db_not_found():
    session = MagicMock()
    session.get.return_value = None

    result = delete_user_in_db(session, 999)

    assert result is None
    session.get.assert_called_once()
