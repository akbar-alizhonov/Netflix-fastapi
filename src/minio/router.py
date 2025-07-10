from typing import Annotated
from fastapi import APIRouter, UploadFile, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
from types_aiobotocore_s3.client import S3Client

from src import User
from src.auth.dependencies import get_current_user
from src.config.dependencies import get_async_session
from src.minio.dependencies import get_s3_client
from src.minio.repository import MinioRepository
from src.minio.service import MinioService

router = APIRouter(tags=["Files"], prefix="/files")


@router.post("/upload_file")
async def upload_file(
        file: UploadFile,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        user: Annotated[User, Depends(get_current_user)],
        s3_client: Annotated[S3Client, Depends(get_s3_client)],
        background_tasks: BackgroundTasks,
):
    s3_repo = MinioRepository(s3_client, "images")
    minio_service = MinioService(session, user, s3_repo)
    try:
        file_id = await minio_service.upload_file(file)
        return {"file_id": file_id}
    finally:
        background_tasks.add_task(s3_client.close)


@router.delete("/file/{file_id}")
async def delete_file(
        file_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        s3_client: Annotated[S3Client, Depends(get_s3_client)],
        background_tasks: BackgroundTasks,
):
    s3_repo = MinioRepository(s3_client, "images")
    minio_service = MinioService(session, user, s3_repo)

    try:
        await minio_service.delete_file(file_id)
        return {"success": "ok"}
    finally:
        background_tasks.add_task(s3_client.close)


@router.get("/file/{file_id}")
async def get_file(
        file_id: int,
        user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)],
        s3_client: Annotated[S3Client, Depends(get_s3_client)],
        background_tasks: BackgroundTasks,
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
        background=background_tasks.add_task(s3_client.close)
    )


@router.put("/file/{file_id}")
async def update_file(
        file_id: int,
        file: UploadFile,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        user: Annotated[User, Depends(get_current_user)],
        s3_client: Annotated[S3Client, Depends(get_s3_client)],
        background_tasks: BackgroundTasks,
):
    s3_repo = MinioRepository(s3_client, "images")
    minio_service = MinioService(session, user, s3_repo)

    try:
        file_id = await minio_service.update_file(file_id, file)
        return {"file_id": file_id}
    finally:
        background_tasks.add_task(s3_client.close)

