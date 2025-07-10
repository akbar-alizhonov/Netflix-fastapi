from fastapi import UploadFile
from types_aiobotocore_s3.client import S3Client

from src.minio.schemas import MinioResponseSchema
from src.minio.utils import generate_filename_and_path


class MinioRepository:
    def __init__(
            self,
            s3_client: S3Client,
            bucket_name: str,
    ):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    async def create(self, file: UploadFile) -> MinioResponseSchema:
        filename, path = generate_filename_and_path(file.content_type)
        await self.s3_client.put_object(
            Body=file.file,
            Bucket=self.bucket_name,
            Key=filename,
            ContentType=file.content_type,
        )

        return MinioResponseSchema(
            filename=filename,
            path=path,
        )

    async def delete(self, filename: str):
        await self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=filename,
        )

    async def update(self, file: UploadFile):
        pass

    async def get(self, filename: str):
        file = await self.s3_client.get_object(
            Bucket=self.bucket_name,
            Key=filename,
        )

        return file["Body"]