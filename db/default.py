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
    """
    Retrieves a single entity of the given model by its ID from the database.

    Args:
    - session: The database session to use.
    - model: The model class of the entity to retrieve.
    - id: The ID of the entity to retrieve.

    Returns:
    - The retrieved entity, or None if it does not exist in the database.
    """
    model_copy = session.get(model, id)
    if not model_copy:
        return None
    return model_copy


def get_all_entities(session: Session, model: type[SQLModel], offset: int = 0, limit: int = 100) -> list[SQLModel]:
    """
    Retrieves all entities of the given model from the database with pagination.

    Args:
    - session: The database session to use.
    - model: The model class of the entities to retrieve.
    - offset: The starting position for the query results. Defaults to 0.
    - limit: The maximum number of results to retrieve. Defaults to 100.

    Returns:
    - A list of retrieved entities.
    """
    model_copy = session.exec(select(model).offset(offset).limit(limit))
    return model_copy


def create_single_entity_by_id(session: Session, model_class: type[SQLModel], create_model: SQLModel):
    """
    Creates a new entity in the database using the provided model class and create model.

    Args:
    - session: The database session to use for the transaction.
    - model_class: The class of the model to be created.
    - create_model: An instance of the model containing the data for the new entity.

    The function validates the create_model against the model_class, adds the new entity to the session, commits the transaction, and refreshes the entity to reflect changes in the database.
    """
    model_copy = model_class.model_validate(create_model)
    session.add(model_copy)
    session.commit()
    session.refresh(model_copy)


def update_single_entity_by_id(session: Session, model_class: type[SQLModel], updated_model: SQLModel, id: int):
    """
    Updates an existing entity in the database using the provided model class and updated model.

    Args:
    - session: The database session to use for the transaction.
    - model_class: The class of the model to be updated.
    - updated_model: An instance of the model containing the updated data for the entity.
    - id: The ID of the entity to be updated.

    The function validates the updated_model against the model_class, updates the existing entity in the session, commits the transaction, and refreshes the entity to reflect changes in the database.

    Returns:
    - The updated entity, or None if the entity does not exist in the database.
    """
    model_copy = get_single_entity_by_id(session, model_class, id)
    if not model_copy:
        return None
    
    for key, value in updated_model.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(model_copy, key, value)
        
    session.commit()
    session.refresh(model_copy)

    return model_copy


def delete_single_entity_by_id(session: Session, model: type[SQLModel], id: int) -> int:
    """
    Deletes an existing entity from the database using the provided model class and ID.

    Args:
    - session: The database session to use for the transaction.
    - model: The class of the model to be deleted.
    - id: The ID of the entity to be deleted.

    The function retrieves the entity from the database using the get_single_entity_by_id function, deletes the entity from the session, commits the transaction, and returns 1 if the entity was successfully deleted, or None if the entity does not exist in the database.

    Returns:
    - 1 if the entity was successfully deleted, or None if the entity does not exist in the database.
    """
    model_copy = get_single_entity_by_id(session, model, id)
    if not model_copy:
        return None
    session.delete(model_copy)
    session.commit()
    return 1
