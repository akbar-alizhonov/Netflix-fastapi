from pydantic import BaseModel


class MinioResponseSchema(BaseModel):
    filename: str
    path: str