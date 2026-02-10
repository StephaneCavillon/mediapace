from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
  database_url: str
  api_key: str
  debug: bool = False
  SECRET_KEY: str = 'dev-secret-key-change-in-production'
  ALGORITHM: str = 'HS256'
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


settings = Settings()  # type: ignore[call-arg]
