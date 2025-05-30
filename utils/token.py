import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from models.token import TokenData
from models.user import UserInDB
from db.users import get_single_user_by_username
from db.session import SessionDep


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


SECRET_KEY = "ab955b6a302b5c2e5b28e3003611ed6a383054f7cbabab71fd3fae34500c87ae"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates an access token using the given data and secret key.

    The token will expire in the given timedelta, or 15 minutes if no timedelta is given.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta | None, optional): The timedelta until the token expires.
            Defaults to None.

    Returns:
        str: The created access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """
    Retrieves the current user from the database using the given token.

    Args:
        session (SessionDep): The SQLModel session to use to interact with the database.
        token (Annotated[str, Depends(oauth2_scheme)]): The token to use for authentication.

    Returns:
        UserInDB: The current user.

    Raises:
        HTTPException: If the credentials are invalid or the user is not found.
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_single_user_by_username(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user