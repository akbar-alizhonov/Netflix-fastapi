from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import async_session_maker


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


