import os
import logging
from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

env = os.environ.get("ENV")
if not env:
    raise Exception("ENV environment variable is not set")

env_file = f".env.{env}"
logging.info(f"Loading environment variables from {env_file}")

dotenv_file = find_dotenv(env_file)
if not dotenv_file:
    raise Exception(f"Environment file {env_file} not found")

load_dotenv(dotenv_file)


class CommonSettings(BaseSettings):
    APP_NAME: str = "FARM Intro"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_ROOT_PATH: str = "/ai-platform/v1"


class DatabaseSettings(BaseSettings):
    DB_URL: str
    DB_NAME: str


class RedisSettings(BaseSettings):
    REDIS_URL: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings, RedisSettings):
    pass


settings = Settings()
