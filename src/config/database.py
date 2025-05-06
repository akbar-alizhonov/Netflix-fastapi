from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config.settings import get_settings

settings = get_settings()

def get_async_engine() -> AsyncEngine:
    engine = create_async_engine(settings.db.url)
    return engine


def get_async_session_maker() -> async_sessionmaker:
    engine = get_async_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return session_maker

async_session_maker = get_async_session_maker()

class Base(DeclarativeBase):
    pass




