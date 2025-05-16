from datetime import datetime, timezone

import jwt
from asyncpg.pgproto.pgproto import timedelta
from passlib.context import CryptContext

from src.auth.exceptions import CredentialsException, TokenExpiredException
from src.config.settings import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_token(token: str) -> dict:
    settings = get_settings()

    try:
        payload = jwt.decode(token, settings.jwt.jwt_secret_key, algorithms=[settings.jwt.algorithm])

        user_id = payload.get("sub")
        if not user_id:
            raise CredentialsException

        expire = payload.get("exp")
        if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
            raise TokenExpiredException

        return payload

    except jwt.InvalidTokenError:
        raise CredentialsException


def generate_token(to_encode: dict, expires_delta: timedelta):
    settings = get_settings()
    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt.jwt_secret_key, algorithm=settings.jwt.algorithm)

    return encoded_jwt