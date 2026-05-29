from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logger import app_logger as logger
from app.core.exceptions.custom_exceptions import BaseAPIException
from fastapi.exceptions import RequestValidationError
from app.core.exceptions.handler import (
    base_api_exception_handler,
    global_exception_handler,
    validation_exception_handler
)


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

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    BaseAPIException,
    base_api_exception_handler
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)

from app.modules.code_review.router import code_review_router
from app.modules.audio_review.router import audio_review_router


app.include_router(code_review_router)
app.include_router(audio_review_router)