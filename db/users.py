from sqlmodel import Session, SQLModel, select

from models.user import UserTable, CreateUser, UserInDB


def get_single_user_by_id(session: Session, id: int) -> UserInDB | None:
    user = session.get(UserTable, id)
    if not user:
        return None
    return UserInDB.model_validate(user)


def get_single_user_by_username(session: Session, username: str) -> UserInDB | None:
    statement = select(UserTable).where(UserTable.username == username)
    user = session.exec(statement).first()
    if not user:
        return None
    return UserInDB.model_validate(user)


def create_user_in_db(session: Session, user: CreateUser) -> UserInDB | None:
    user_table = UserTable.from_create_user(user)
    session.add(user_table)
    session.commit()
    session.refresh(user_table)
    return UserInDB.model_validate(user_table)


def update_user_in_db(session: Session, new_user: CreateUser, id: int) -> SQLModel:
    old_user = get_single_user_by_id(session, id)
    if not old_user:
        return None
    for key, value in new_user.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(old_user, key, value)
    session.commit()
    session.refresh(old_user)
    return old_user


def delete_user_in_db(session: Session, id: int) -> int:
    user = get_single_user_by_id(session, id)
    if not user:
        return None
    session.delete(user)
    session.commit()
    return 1
