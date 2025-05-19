from datetime import timedelta

from redis.asyncio import Redis

from src.auth.utils import generate_token
from src.config.settings import get_settings


class TokenDAO:

    def __init__(self, redis: Redis):
        self.redis = redis

    def generate_access_token(self, user_id: int, username: str) -> str:
        settings = get_settings()
        to_encode = {
            "sub": str(user_id),
            "username": username,
        }

        access_token = generate_token(
            to_encode,
            expires_delta=timedelta(minutes=settings.jwt.access_token_expire_minutes)
        )

        return access_token

    def generate_refresh_token(self, user_id: int) -> str:
        settings = get_settings()
        to_encode = {"sub": str(user_id)}

        refresh_token = generate_token(to_encode, expires_delta=timedelta(days=settings.jwt.refresh_token_expire_days))

        return refresh_token

    async def save_refresh_token(self, user_id: int, refresh_token: str) -> None:
        settings = get_settings()
        await self.redis.set(refresh_token, user_id, ex=timedelta(days=settings.jwt.refresh_token_expire_days))

    async def delete_refresh_token(self, refresh_token: str) -> None:
        await self.redis.delete(refresh_token)

    async def generate_new_refresh_token_and_access_token(
            self,
            user_id: int,
            username: str,
            refresh_token: str | None = None,
    ) -> dict[str, str]:
        if refresh_token:
            await self.delete_refresh_token(refresh_token)

        access_token = self.generate_access_token(user_id, username)
        refresh_token = self.generate_refresh_token(user_id)
        await self.save_refresh_token(user_id, refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }






