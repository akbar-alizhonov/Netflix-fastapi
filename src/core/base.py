from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User


class Base:
    def __init__(self, session: AsyncSession, current_user: User | None = None):
        self._session = session
        self._current_user = current_user