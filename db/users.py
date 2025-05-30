from sqlmodel import Session, select

from models.user import UserTable, CreateUser, UserInDB, UpdateUser


def get_all_users_in_db(session: Session) -> list[UserInDB]:
    """
    Retrieves all users from the database.

    Args:
        session (Session): The SQLModel session to use to interact with the database.

    Returns:
        A list of `UserInDB` objects representing all users in the database.
    """
    users = session.exec(select(UserTable)).all()
    return [UserInDB.model_validate(user) for user in users]


def get_single_user_by_id(session: Session, id: int) -> UserInDB | None:
    """
    Retrieves a single user from the database by their ID.

    Args:
        session (Session): The SQLModel session to use to interact with the database.
        id (int): The ID of the user to be retrieved.

    Returns:
        UserInDB | None: A `UserInDB` object representing the user if found, otherwise None.
    """
    user = session.get(UserTable, id)
    if not user:
        return None
    return UserInDB.model_validate(user)


def get_single_user_by_username(session: Session, username: str) -> UserInDB | None:
    """
    Retrieves a single user from the database by their username.

    Args:
        session (Session): The SQLModel session to use to interact with the database.
        username (str): The username of the user to be retrieved.

    Returns:
        UserInDB | None: A `UserInDB` object representing the user if found, otherwise None.
    """
    statement = select(UserTable).where(UserTable.username == username)
    user = session.exec(statement).first()
    if not user:
        return None
    return UserInDB.model_validate(user)


def create_user_in_db(session: Session, user: CreateUser) -> UserInDB | None:
    """
    Creates a new user in the database.

    Args:
        session (Session): The SQLModel session to use to interact with the database.
        user (CreateUser): The data for the new user to be created.

    Returns:
        UserInDB | None: A `UserInDB` object representing the newly created user if the creation was successful, otherwise None.
    """
    user_table = UserTable.from_create_user(user)

    session.add(user_table)
    session.commit()
    session.refresh(user_table)

    return UserInDB.model_validate(user_table)


def update_user_in_db(session: Session, updated_user: UpdateUser, user_id: int) -> UserInDB | None:
    """
    Updates an existing user in the database.

    Args:
        session (Session): The SQLModel session to use to interact with the database.
        updated_user (UpdateUser): The data for the user to be updated.
        user_id (int): The ID of the user to be updated.

    Returns:
        UserInDB | None: A `UserInDB` object representing the updated user if the update was successful, otherwise None.
    """
    user_table = session.get(UserTable, user_id)

    if not user_table:
        return None
    
    hero_data = updated_user.model_dump(exclude_unset=True, exclude_none=True)

    user_table.sqlmodel_update(hero_data)
    session.add(user_table)
    session.commit()
    session.refresh(user_table)

    return UserInDB.model_validate(user_table)


def delete_user_in_db(session: Session, id: int) -> int:
    """
    Deletes an existing user from the database.

    Args:
        session (Session): The SQLModel session to use to interact with the database.
        id (int): The ID of the user to be deleted.

    Returns:
        int | None: 1 if the deletion was successful, otherwise None.
    """
    user = session.get(UserTable, id)
    if not user:
        return None
    session.delete(user)
    session.commit()
    return 1
