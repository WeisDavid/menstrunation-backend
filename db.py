import os

from typing import Annotated
from pydantic import ConfigDict

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine, select


maria_url = os.getenv("DATABASE_URL")
engine = create_engine(maria_url)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_single_entity_by_id(session: Session, model: type[SQLModel], id: int) -> SQLModel:
    model_copy = session.get(model, id)
    if not model_copy:
        return None
    return model_copy


def get_all_entities(session: Session, model: type[SQLModel], offset: int = 0, limit: int = 100) -> list[SQLModel]:
    model_copy = session.exec(select(model).offset(offset).limit(limit))
    return model_copy


def create_single_entity_by_id(session: Session, model_class: type[SQLModel], create_model: SQLModel):
    model_copy = model_class.model_validate(create_model)
    session.add(model_copy)
    session.commit()
    session.refresh(model_copy)


def update_single_entity_by_id(session: Session, model_class: type[SQLModel], updated_model: SQLModel, id: int):
    model_copy = get_single_entity_by_id(session, model_class, id)
    if not model_copy:
        return None
    
    for key, value in updated_model.model_dump(exclude_unset=True).items():
        setattr(model_copy, key, value)
        
    session.commit()
    session.refresh(model_copy)

    return model_copy


def delete_single_entity_by_id(session: Session, model: type[SQLModel], id: int) -> int:
    model_copy = get_single_entity_by_id(session, model, id)
    if not model_copy:
        return None
    session.delete(model_copy)
    session.commit()
    return 1
