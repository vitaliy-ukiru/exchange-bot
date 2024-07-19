from typing import Annotated

from pydantic import SecretStr, RedisDsn, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    bot_token: SecretStr
    redis_url: Annotated[RedisDsn, Field(default="redis://localhost:6379/0")]
    redis_prefix: Annotated[str, Field(default="cbr-exchange-bot")]
    force_reload_rates_minutes: int = 12 * 60  # once time at 12 hours
    update_rates_cron: Annotated[str, Field(default="0 0 * * *")]  # every day at 12:00 AM

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8"
    )
