from sqlmodel import Session, SQLModel, select

from models.user import UserTable, CreateUser, UserInDB, UpdateUser


def get_all_users_in_db(session: Session) -> list[UserInDB]:
    users = session.exec(select(UserTable)).all()
    return [UserInDB.model_validate(user) for user in users]


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


def update_user_in_db(session: Session, updated_user: UpdateUser, user_id: int) -> UserInDB | None:
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
    user = session.get(UserTable, id)
    if not user:
        return None
    session.delete(user)
    session.commit()
    return 1
