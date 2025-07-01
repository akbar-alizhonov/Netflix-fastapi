from typing import Annotated

from botocore.client import BaseClient
from fastapi import APIRouter, UploadFile, Depends

from src.minio.dependencies import get_s3_client

router = APIRouter(tags=["Video"], prefix="/static")


@router.post("/upload_file")
async def upload_film(
        file: UploadFile,
        s3_client: Annotated[BaseClient, Depends(get_s3_client)]
):
    pass
