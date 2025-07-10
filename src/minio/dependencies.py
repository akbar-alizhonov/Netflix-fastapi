from aiobotocore.session import get_session
from botocore.exceptions import BotoCoreError
from types_aiobotocore_s3.client import S3Client
from loguru import logger

from src.config.settings import get_settings


async def get_s3_client() -> S3Client:
    session = get_session()
    settings = get_settings()

    try:
        async with session.create_client(
                "s3",
                endpoint_url=settings.s3.minio_endpoint,
                aws_access_key_id=settings.s3.minio_access_key,
                aws_secret_access_key=settings.s3.minio_secret_key,
        ) as s3_client:
            return s3_client

    except BotoCoreError as e:
        logger.error(e)
        raise e