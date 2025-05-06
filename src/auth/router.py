from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src import User
from src.auth.dao import AuthDAO
from src.auth.repository import AuthRepository
from src.auth.schemas import UserCreateSchema, TokenSchema
from src.config.dependencies import get_async_session
from src.auth.dependencies import get_current_user

router = APIRouter(tags=["Аутентификация & Авторизация"], prefix="/auth")

@router.post("/register")
async def register_user(
        user_data: Annotated[UserCreateSchema, Depends()],
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    repo = AuthRepository(session)
    auth_dao = AuthDAO(session, repo=repo)
    await auth_dao.add(user_data)


@router.post("/login")
async def login(
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    auth_dao = AuthDAO(session)
    user = await auth_dao.authenticate(user_data)
    access_token = auth_dao.create_access_token(user)

    return TokenSchema(access_token=access_token, token_type="bearer")


@router.get("/me")
async def get_me(
        user: Annotated[User, Depends(get_current_user)],
):
    return user