from loguru import logger

from src.auth.schemas import UserCreateSchema
from src.auth.models import User
from src.core.repository import RepositoryBase


class AuthRepository(RepositoryBase):

    async def create(self, user_data: UserCreateSchema):
        logger.info(f"CREATE USER {user_data.username}")
        user = User(**user_data.model_dump())
        self._session.add(user)
        await self._session.commit()

    async def update(self, user: User) -> User:
        pass

    async def delete(self, user: User) -> User:
        pass

    async def get(self, user_id: int) -> User | None:
        user = await self._session.get(User, user_id)
        return user

