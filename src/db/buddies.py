from sqlmodel import Session, select

from db.users import get_single_user_by_id
from models.buddy import BuddyCreate, BuddyTable, BuddyInDB
from models.user import UserInDB


def get_buddy_by_id(session: Session, buddy_id: int):
    buddy = session.get(BuddyTable, buddy_id)
    if not buddy:
        return None
    return BuddyInDB.model_validate(buddy)

def create_buddy_in_db(session: Session, buddy: BuddyCreate):
    validated_buddy = BuddyTable.model_validate(buddy)
    session.add(validated_buddy)
    session.commit()
    session.refresh(validated_buddy)
    return BuddyInDB.model_validate(validated_buddy).id

def get_buddies_by_id(session: Session, user_id: int):
    statement_self = select(BuddyTable).where(BuddyTable.userID1 == user_id)
    statement_other = select(BuddyTable).where(BuddyTable.userID2 == user_id)

    buddies_by_self = session.exec(statement_self).all()
    buddies_by_other = session.exec(statement_other).all()

    if not buddies_by_self and not buddies_by_other:
        return None

    buddy_users = []

    for buddies in buddies_by_self:
        self_buddy = get_single_user_by_id(session, buddies.userID2)
        buddy_users.append(UserInDB.model_validate(self_buddy))

    for buddies in buddies_by_other:
        other_buddy = get_single_user_by_id(session, buddies.userID1)
        buddy_users.append(UserInDB.model_validate(other_buddy))

    return buddy_users

def delete_buddies_by_id(session: Session, buddy_id: int):
    buddy = session.get(BuddyTable, buddy_id)
    if not buddy:
        return None
    session.delete(buddy)
    session.commit()
    return 1