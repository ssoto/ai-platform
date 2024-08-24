import os
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv


env = os.environ.get('ENV', "local")
env_file = f".env.{env}"
load_dotenv(find_dotenv(env_file))


class CommonSettings(BaseSettings):
    APP_NAME: str = "FARM Intro"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_ROOT_PATH: str = "/freepik/ai-platform/v1"


class DatabaseSettings(BaseSettings):
    DB_URL: str
    DB_NAME: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
