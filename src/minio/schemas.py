from typing import Any

from pydantic import BaseModel


class MinioResponseSchema(BaseModel):
    filename: str
    path: str


class FileSchema(BaseModel):
    filename: str
    content_type: str
    content: Any
