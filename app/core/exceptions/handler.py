from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.exceptions.custom_exceptions import (
    BaseAPIException
)

async def base_api_exception_handler(
    request: Request,
    exc: BaseAPIException
):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": {
                "success": False,
                "error_message": exc.message
            },
            "evaluations": []
        }
    )


async def global_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content={
            "status": {
                "success": False,
                "error_message": (
                    "Unexpected internal server error"
                )
            },
            "evaluations": []
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    first_error = exc.errors()[0]

    field_name = first_error["loc"][-1]

    message = (
        f"Field '{field_name}' "
        f"is required"
    )

    return JSONResponse(
        status_code=422,
        content={
            "status": {
                "success": False,
                "error_message": message
            },
            "evaluations": []
        }
    )