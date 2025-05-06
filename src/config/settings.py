
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
    algorithm: str = Field("HS256")


class Settings:
    db = DBSettings()
    jwt = JWTSettings()


def get_settings():
    return Settings()