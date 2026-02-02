from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  database_url: str
  api_key: str
  debug: bool = False

  model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
