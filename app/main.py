from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import app_logger as logger


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Review AI service started")

    yield

    logger.info("Review AI service stopped")


app = FastAPI(
    title="Review AI",
    version="1.0.0",
    lifespan=lifespan
)