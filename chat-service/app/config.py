from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    database_url: str
    openai_api_key: SecretStr
    llm_model: str = "gpt-4o-mini"
    system_prompt: str = "You are a helpful assistant."
    cors_origins: list[str] = ["http://localhost:3000"]
    sentry_dsn: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


app_settings = AppSettings()
