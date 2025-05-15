from datetime import datetime, timezone

import jwt
from asyncpg.pgproto.pgproto import timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, or_

from src import User
from src.auth.exceptions import UserUsernameAlreadyExistException, UserEmailAlreadyExistException
from src.auth.schemas import UserCreateSchema
from src.auth.utils import get_password_hash, verify_password
from src.core.dao import DAOBase
from src.config.settings import get_settings


class AuthDAO(DAOBase):

    async def get_user_by_username_or_none(self, username: str) -> User | None:
        user = await self._session.execute(
            select(User).where(User.username == username)
        )

        return user.scalars().first()

    async def get_user_by_email_or_none(self, email: str) -> User | None:
        user = await self._session.execute(
            select(User).where(User.email == email)
        )

        return user.scalars().first()

    async def add(self, user_data: UserCreateSchema):
        existing_user_by_username = await self.get_user_by_username_or_none(user_data.username)
        if existing_user_by_username:
            raise UserUsernameAlreadyExistException

        existing_user_by_email = await self.get_user_by_email_or_none(user_data.email)
        if existing_user_by_email:
            raise UserEmailAlreadyExistException

        hashed_password = get_password_hash(user_data.password)
        user_data.password = hashed_password

        await self.repo.create(user_data)

    async def get_user(self, username: str):
        user = await self._session.execute(
            select(User)
            .where(
                or_(
                    User.username == username,
                    User.email == username,
                )
            )
        )

        return user.scalar_one_or_none()

    async def authenticate(self, user_data: OAuth2PasswordRequestForm) -> User | None:
        user = await self.get_user(user_data.username)
        if not user:
            return

        if not verify_password(user_data.password, user.password):
            return

        return user

    def create_access_token(self, user: User):
        settings = get_settings()
        to_encode = {}
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.access_token_expire_minutes)
        to_encode.update(
            {
                "user_id": user.id,
                "username": user.username,
                "exp": expire
            }
        )
        encoded_jwt = jwt.encode(to_encode, settings.jwt.jwt_secret_key, algorithm=settings.jwt.algorithm)

        return encoded_jwt


