from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    surname: str | None = None
    birthday: datetime | None = None
    email: EmailStr
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str