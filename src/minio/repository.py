import aioboto3
from botocore.client import BaseClient
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src import User
from src.core.repository import RepositoryBase


class MinioRepository(RepositoryBase):
    def __init__(
            self,
            *,
            s3_client: BaseClient,
            session: AsyncSession | None = None,
            current_user: User | None = None,
    ):
        super().__init__(session, current_user)

    async def create(self, file: UploadFile):
        pass