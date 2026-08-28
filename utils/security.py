import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt, JWTError

load_dotenv()

# --------------------------------------------------
# this part is used for password hashing
# --------------------------------------------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# --------------------------------------------------
# it is used for creating the JWT tokens
# --------------------------------------------------
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)
JWT_EXPIRATION_MINUTES = int(
    os.getenv(
        "JWT_EXPIRATION_MINUTES",
        "60"
    )
)
if not JWT_SECRET_KEY:
    raise ValueError(
        "JWT_SECRET_KEY is not configured in .env"
    )

# --------------------------------------------------
# Hash the password gets from the user
# --------------------------------------------------
def hash_password(password: str) -> str:
    """
    the password given by user was hashed
    """
    return pwd_context.hash(password)

# --------------------------------------------------
# Verify whether the password is crt and belongs to that mail id
# --------------------------------------------------
def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    """it verifies whether the password is correct for that mail id
    """
    return pwd_context.verify(
        plain_password,
        hashed_password
    )