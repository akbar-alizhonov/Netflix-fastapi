from abc import ABC, abstractmethod

from src.core.base import Base


class RepositoryBase(Base, ABC):

    @abstractmethod
    async def create(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError