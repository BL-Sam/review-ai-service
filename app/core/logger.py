import sys
from pathlib import Path

from loguru import logger


# Create logs directory
LOG_DIR = Path("logs")

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "review_ai.log"


class LoggerConfig:

    @staticmethod
    def setup_logger():

        # Remove default logger
        logger.remove()

        # Console Logger
        logger.add(
            sys.stdout,
            level="INFO",
            colorize=True,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:"
                "<cyan>{function}</cyan>:"
                "<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            )
        )

        # File Logger
        logger.add(
            LOG_FILE,
            level="DEBUG",
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            enqueue=True,
            backtrace=True,
            diagnose=True,
            encoding="utf-8",
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level: <8} | "
                "{name}:{function}:{line} | "
                "{message}"
            )
        )

        return logger


app_logger = LoggerConfig.setup_logger()