from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import CredentialsException, TokenExpiredException
from src.auth.repository import AuthRepository
from src.config.dependencies import get_async_session
from src.config.settings import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        token: Annotated[str, Depends(oauth2_scheme)]
):
    settings = get_settings()

    try:
        payload = jwt.decode(token, settings.jwt.jwt_secret_key, algorithms=[settings.jwt.algorithm])

        user_id = payload.get("user_id")
        if not user_id:
            raise CredentialsException

    except jwt.InvalidTokenError:
        raise CredentialsException

    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise TokenExpiredException

    auth_repo = AuthRepository(session)

    user = await auth_repo.get(user_id)
    if not user:
        raise CredentialsException

    return user

