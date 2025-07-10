from typing import Type, TypeVar, Union

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

T = TypeVar("T", bound=DeclarativeBase)

async def get_object_or_404(
        session: AsyncSession,
        model: Type[T],
        pk: int,
        message: str = "Такая запись не найдена в бд"
) -> Type[T] | None:
    """
        Получает объект из БД по первичному ключу или вызывает 404 ошибку.

        Args:
            session: Асинхронная сессия SQLAlchemy
            model: Класс модели SQLAlchemy
            pk: Первичный ключ объекта
            message: Сообщение, которое будет выдаваться в случае ошибки

        Returns:
            Экземпляр запрошенной модели

        Raises:
            HTTPException: 404 если объект не найден
        """
    instance = await session.get(model, pk)
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )

    return instance
