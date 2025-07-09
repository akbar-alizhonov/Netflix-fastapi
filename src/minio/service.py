from fastapi import UploadFile
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src import User, File
from src.core.service import ServiceBase
from src.core.utils import get_object_or_404
from src.minio.repository import MinioRepository


class MinioService(ServiceBase):
    def __init__(
            self,
            session: AsyncSession,
            current_user: User,
            repo: MinioRepository
    ):
        super().__init__(session, current_user)
        self.repo = repo

    async def upload_file(self, file: UploadFile):
        resp = await self.repo.create(file)
        new_file = File(
            filename=resp.filename,
            path=resp.path,
            bucket_name=self.repo.bucket_name,
            content_type=file.content_type,
        )

        self._session.add(new_file)
        await self._session.flush()
        await self._session.commit()
        logger.info(f"UPLOAD FILE [{resp.filename}] ID [{new_file.id}]")

        return new_file.id

    async def delete(self, file_id):
        file: File = await get_object_or_404(self._session, File, file_id)
        resp = await self.repo.delete(file.filename)

        await self._session.delete(file)
        await self._session.commit()
        logger.info(f"DELETE FILE [{file.filename}] ID [{file_id}]")

