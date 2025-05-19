from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src import User
from src.core.base import Base
from src.core.repository import RepositoryBase


class DAOBase(Base):
    def __init__(
            self,
            session: AsyncSession,
            current_user: User | None = None,
            repo: RepositoryBase | None = None,
    ):
        super().__init__(session, current_user)
        self.repo = repo