from types_aiobotocore_s3.client import S3Client
from botocore.session import get_session
from loguru import logger

from src.config.settings import get_settings


async def get_s3_client() -> S3Client:
    session = get_session()
    settings = get_settings()

    async with session.create_client(
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
