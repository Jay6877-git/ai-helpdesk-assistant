import os
from datetime import datetime, timedelta, UTC

from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext


# Central password hashing configuration. `deprecated="auto"` lets passlib
# transparently flag old hashes if the configured scheme changes later.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

load_dotenv()

# JWT settings are read once at import time so token creation and validation use
# the same algorithm, secret, and expiry window across the app.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: dict) -> str:
    """Create a signed access token that carries the supplied claims."""
    to_encode = data.copy()

    # Store the expiry as a timezone-aware UTC timestamp for jose/jwt.
    expire_time = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    """Return token claims when validation succeeds, otherwise return None."""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def hash_password(password: str) -> str:
    """Hash a plaintext password before persisting it."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare a submitted password with the stored password hash."""
    return pwd_context.verify(plain_password, hashed_password)
