import os
from dotenv import load_dotenv
from app.core.logger import app_logger as logger
from pydantic_settings import BaseSettings

load_dotenv()


class BaseConfig(BaseSettings):
    ENV: str = os.getenv("ENV", "DEV")
    REVIEW_AI_API_TOKEN: str = os.getenv("REVIEW_AI_API_TOKEN", "DEV")

    GEMINI_MODEL: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash-lite"
    )

    GEMINI_API_KEY: str = os.getenv(
        "GEMINI_API_KEY"
    )

    GEMINI_TEMPERATURE: float = float(
        os.getenv("GEMINI_TEMPERATURE", 0.0)
    )

    DEBUG: bool = False


class DevConfig(BaseConfig):
    DEBUG: bool = True
    GEMINI_TEMPERATURE: float = 0.0
    LOCAL_AUDIO_BASE_PATH: str = "./audio_files"


class ProdConfig(BaseConfig):
    DEBUG: bool = False
    GEMINI_TEMPERATURE: float = 0.0


# instantiate once to read ENV
base_config = BaseConfig()

# pick config based on ENV
settings = (
    DevConfig()
    if base_config.ENV.upper() == "DEV"
    else ProdConfig()
)

logger.info(
    f"Environment variables initialized: {settings.ENV}"
)