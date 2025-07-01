from botocore.client import BaseClient
from fastapi import UploadFile
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src import User
from src.core.repository import RepositoryBase
from src.minio.models import File
from src.minio.utils import generate_filename_and_path


class MinioRepository(RepositoryBase):
    def __init__(
            self,
            session: AsyncSession,
            current_user: User,
            s3_client: BaseClient,
            bucket_name: str,
    ):
        super().__init__(session, current_user)
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    async def create(self, file: UploadFile):
        try:
            filename, path = generate_filename_and_path(file.content_type)

            await self.s3_client.put_object(
                Body=await file.read(),
                Bucket=self.bucket_name,
                Key=filename,
                ContentType=file.content_type,
            )

            new_file = File(
                filename=filename,
                path=path,
                bucket_name=self.bucket_name,
                content_type=file.content_type,
            )

            self._session.add(new_file)
            await self._session.flush()
            await self._session.commit()

            return new_file.id

        except Exception as e:
            logger.error(f"ERROR WHILE UPLOADING {file.filename}")
            raise e

    async def delete(self, file: UploadFile):
        pass

    async def update(self, file: UploadFile):
        pass

    async def get(self, *args, **kwargs):
        pass
