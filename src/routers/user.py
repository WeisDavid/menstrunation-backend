from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated

from db.session import SessionDep
from models.user import CreateUser, UserInDB, UserResponse, UpdateUser
from models.token import Token
from db.users import get_single_user_by_username, create_user_in_db, update_user_in_db, delete_user_in_db, get_all_users_in_db
from utils.token import get_current_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from utils.pw_auth import verify_password

from datetime import timedelta


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends()
    ],
    session: SessionDep
):
    user = get_single_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=token, token_type="bearer")


@router.get("/get", response_model=UserResponse)
def read_me(
    current_user: Annotated[
        UserInDB,
        Depends(get_current_user)
    ],
    session: SessionDep
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.get("/all", response_model=list[UserResponse])
def read_all(
    current_user: Annotated[
        UserInDB,
        Depends(get_current_user)
    ],
    session: SessionDep
) -> list[UserResponse]:
    return [UserResponse.model_validate(user) for user in get_all_users_in_db(session)]


@router.post("/create", response_model=Token)
def create_user(
    user: CreateUser,
    session: SessionDep
) -> Token:
    # 1. Create the user
    created_user = create_user_in_db(session, user)
    if not created_user:
        raise HTTPException(status_code=400, detail="Invalid user data")

    # 2. Generate access token using user ID and/or username
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"sub": created_user.id},  # or add "username": created_user.username
        expires_delta=access_token_expires
    )

    # 3. Return token just like /token does
    return Token(access_token=token, token_type="bearer")


@router.put("/update", response_model=UserResponse)
def update_user(
    current_user: Annotated[
        UserInDB,
        Depends(get_current_user)
    ],
    updated_user: UpdateUser,
    session: SessionDep
) -> UserResponse:
    response = UserResponse.model_validate(update_user_in_db(session, updated_user, current_user.id))
    return response
            

@router.delete("/delete")
def user_delete(
    current_user: Annotated[
        UserInDB,
        Depends(get_current_user)
    ],
    session: SessionDep
):
    user_id = current_user.id
    deleted = delete_user_in_db(session, user_id)
    if deleted is None: 
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    return JSONResponse(status_code=204, content={"message": f"User with ID {user_id} deleted successfully."})
