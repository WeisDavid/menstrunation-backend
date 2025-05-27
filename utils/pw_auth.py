from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a plain password
def get_password_hash(password: str) -> str:
    """
    Hash a plain password.

    Args:
    - password (str): The plain password to hash.

    Returns:
    - str: The hashed password.
    """
    return pwd_context.hash(password)


# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
    - plain_password (str): The plain password to verify.
    - hashed_password (str): The hashed password to verify against.

    Returns:
    - bool: Whether the plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)
