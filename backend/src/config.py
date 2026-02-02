from pydantic_settings import BaseSettings
# from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # model_config = SettingsConfigDict( env_file=".env", env_file_encoding="utf-8" ) # en attendant de comprendre l'utilisation de la classe Config
    database_url: str
    api_key: str
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



