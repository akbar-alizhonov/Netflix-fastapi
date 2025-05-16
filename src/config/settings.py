
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class DBSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='.env',
        extra="ignore"
    )

    db_port: int = Field(5432)
    db_name: str = Field("postgres")
    db_user: str = Field("postgres")
    db_password: str = Field("postgres")
    db_host: str = Field("localhost")

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra="ignore"
    )

    jwt_secret_key: str
    access_token_expire_minutes: int = Field(15)
    refresh_token_expire_days: int = Field(1)
    algorithm: str = Field("HS256")


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra="ignore"
    )

    redis_host: str
    redis_port: int = Field(6379)
    redis_password: str
    redis_user: str
    redis_db: int = Field(0)

    @property
    def url(self) -> str:
        return f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"


class Settings:
    db = DBSettings()
    jwt = JWTSettings()
    redis = RedisSettings()


def get_settings():
    return Settings()