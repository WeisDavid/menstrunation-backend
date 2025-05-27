from sqlmodel import Session, select

from models.buddy import BuddyCreate, BuddyTable, BuddyInDB

def get_buddy_by_id(session: Session, buddy_id: int):
    buddy = session.get(BuddyTable, buddy_id)
    if not buddy:
        return None
    return BuddyInDB.model_validate(buddy)

def create_buddy_in_db(session: Session, buddy: BuddyCreate):
    validated_buddy = BuddyCreate.model_validate(buddy)
    session.add(validated_buddy)
    session.commit()
    session.refresh(validated_buddy)
    return BuddyInDB.model_validate(validated_buddy).id

def get_buddies_by_id(session: Session, user_id: int):
    statement_self = select(BuddyTable).where(BuddyTable.benutzer_id_1 == user_id)
    statement_other = select(BuddyTable).where(BuddyTable.benutzer_id_2 == user_id)

    buddies_by_self = session.exec(statement_self)
    buddies_by_other = session.exec(statement_other)

    if not buddies_by_self and not buddies_by_other:
        return None

    return None

def delete_buddies_by_id(session: Session, buddy_id: int):
    buddy = get_buddy_by_id(session, buddy_id)
    if not buddy:
        return None
    session.delete(buddy)
    session.commit()
    return 1