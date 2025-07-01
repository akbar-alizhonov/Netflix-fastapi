from typing import Annotated
from botocore.client import BaseClient
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import User
from src.auth.dependencies import get_current_user
from src.config.dependencies import get_async_session
from src.minio.dependencies import get_s3_client
from src.minio.repository import MinioRepository

router = APIRouter(tags=["File"], prefix="/file")


@router.post("/upload_image")
async def upload_image(
        file: UploadFile,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        user: Annotated[User, Depends(get_current_user)],
        s3_client: Annotated[BaseClient, Depends(get_s3_client)]
):
    s3_repo = MinioRepository(
        session, user, s3_client, "images"
    )
    response = await s3_repo.create(file)

    return response

