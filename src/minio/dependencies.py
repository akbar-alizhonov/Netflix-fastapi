import aioboto3
from botocore.client import BaseClient
from loguru import logger

from src.config.settings import get_settings


async def get_s3_client() -> BaseClient:
    session = aioboto3.Session()
    settings = get_settings()

    async with session.client(
        "s3",
        endpoint_url=settings.s3.minio_endpoint,
        aws_access_key_id=settings.s3.minio_access_key,
        aws_secret_access_key=settings.s3.minio_secret_key,
    ) as client:
        try:
            yield client
        except Exception as e:
            logger.error(e)
        finally:
            await client.close()
