from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from app.core.config import settings

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy")

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)

def create_access_token(user_id: int) -> tuple[str, datetime]:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"user_id": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM), expire

def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload is None:
            return None
        return payload
    except InvalidTokenError:
        return None