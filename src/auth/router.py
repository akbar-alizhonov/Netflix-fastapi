from typing import Annotated

from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src import User
from src.auth.daos.auth import AuthDAO
from src.auth.daos.token import TokenDAO
from src.auth.exceptions import IncorrectUsernameOrPasswordException, RefreshTokenNotFound, UserNotFoundFromRefreshToken
from src.auth.repository import AuthRepository
from src.auth.schemas import UserCreateSchema, TokenSchema
from src.config.dependencies import get_async_session, get_redis
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


@router.post("/login", response_model=TokenSchema)
async def login(
        response: Response,
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        redis: Annotated[Redis, Depends(get_redis)],
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    auth_dao = AuthDAO(session)

    user = await auth_dao.authenticate(user_data)
    if not user:
        raise IncorrectUsernameOrPasswordException

    token_dao = TokenDAO(redis)
    tokens = await token_dao.generate_new_refresh_token_and_access_token(user.id, user.username)
    response.set_cookie("refresh_token", tokens.get("refresh_token"), httponly=True)

    return TokenSchema(access_token=tokens.get("access_token"), token_type="bearer")


@router.post("/logout")
async def logout(
        response: Response,
        request: Request,
        user: Annotated[User, Depends(get_current_user)],
        redis: Annotated[Redis, Depends(get_redis)],
        session: Annotated[AsyncSession, Depends(get_async_session)]
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise RefreshTokenNotFound

    token_dao = TokenDAO(redis=redis)
    response.delete_cookie("refresh_token")
    await token_dao.delete_refresh_token(refresh_token, redis)


@router.get("/me")
async def get_me(
        user: Annotated[User, Depends(get_current_user)],
):
    return user


@router.post("/refresh_token", response_model=TokenSchema)
async def new_refresh_token(
        response: Response,
        request: Request,
        session: Annotated[AsyncSession, Depends(get_async_session)],
        user: Annotated[User, Depends(get_current_user)],
        redis: Annotated[Redis, Depends(get_redis)],
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise RefreshTokenNotFound

    auth_dao = AuthDAO(session)

    user = await auth_dao.get_user_by_refresh_token(refresh_token, redis)
    if not user:
        raise UserNotFoundFromRefreshToken

    token_dao = TokenDAO(redis)
    tokens = await token_dao.generate_new_refresh_token_and_access_token(user.id, user.username, refresh_token)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return TokenSchema(access_token=tokens.get("access_token"), token_type="bearer")
