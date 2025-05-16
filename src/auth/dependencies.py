from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import CredentialsException, TokenExpiredException
from src.auth.repository import AuthRepository
from src.auth.utils import validate_token
from src.config.dependencies import get_async_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        session: Annotated[AsyncSession, Depends(get_async_session)],
        token: Annotated[str, Depends(oauth2_scheme)]
):
    try:
        payload = validate_token(token)
        auth_repo = AuthRepository(session)

        user = await auth_repo.get(int(payload.get("sub")))
        if not user:
            raise CredentialsException

        return user

    except (CredentialsException, TokenExpiredException) as e:
        raise e

