import redis.asyncio as aioredis

from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import async_session_maker
from src.config.settings import get_settings


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_redis():
    settings = get_settings()
    redis = aioredis.from_url(settings.redis.url, decode_responses=True)

    try:
        await redis.ping()
        yield redis
    finally:
        await redis.close()
