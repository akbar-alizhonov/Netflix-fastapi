from fastapi import UploadFile
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src import User, File
from src.core.service import ServiceBase
from src.core.utils import get_object_or_404
from src.minio.repository import MinioRepository
from src.minio.schemas import FileSchema


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

    async def delete_file(self, file_id):
        file = await get_object_or_404(self._session, File, file_id)

        await self.repo.delete(file.filename)
        await self._session.delete(file)
        await self._session.commit()

        logger.info(f"DELETE FILE [{file.filename}] ID [{file_id}]")

    async def get_file(self, file_id) -> FileSchema:
        file = await get_object_or_404(self._session, File, file_id)
        resp = await self.repo.get(file.filename)

        return FileSchema(
            filename=file.filename,
            content_type=file.content_type,
            content=resp
        )

    async def update_file(self, file_id: int, file: UploadFile):
        old_file = await get_object_or_404(self._session, File, file_id)
        resp = await self.repo.update(old_file.filename, file)

        old_filename = old_file.filename
        old_file.filename = resp.filename
        old_file.content_type = file.content_type

        await self._session.commit()
        logger.info(f"UPDATE FILE ID [{old_file.id}] OLD FILENAME [{old_filename}] NEW FILENAME [{old_file.filename}]")

        return old_file.id


