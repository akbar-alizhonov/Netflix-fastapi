from typing import Annotated
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
from types_aiobotocore_s3.client import S3Client

from src import User
from src.auth.dependencies import get_current_user
from src.config.dependencies import get_async_session
from src.minio.dependencies import get_s3_client
from src.minio.repository import MinioRepository
from src.minio.service import MinioService

router = APIRouter(tags=["File"], prefix="/file")


@router.post("/upload_image")
async def upload_image(
        file: UploadFile,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        user: Annotated[User, Depends(get_current_user)],
        s3_client: Annotated[S3Client, Depends(get_s3_client)]
):
    s3_repo = MinioRepository(s3_client, "images")
    minio_service = MinioService(session, user, s3_repo)
    file_id = await minio_service.upload_file(file)

    return {"file_id": file_id}


@router.delete("/image/{file_id}")
async def delete_image(
        file_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        s3_client: Annotated[S3Client, Depends(get_s3_client)]
):
    s3_repo = MinioRepository(s3_client, "images")
    minio_service = MinioService(session, user, s3_repo)
    await minio_service.delete_file(file_id)

    return {"success": "ok"}


@router.get("/image/{file_id}")
async def get_image(
        file_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        s3_client: Annotated[S3Client, Depends(get_s3_client)]
):
    s3_repo = MinioRepository(s3_client, "images")
    minio_service = MinioService(session, user, s3_repo)
    file = await minio_service.get_file(file_id)

    return StreamingResponse(
        content=file.content.iter_chunks(),
        media_type=file.content_type,
        headers={
            'Content-Disposition': f'attachment; filename="{file.filename}"'
        },
    )


