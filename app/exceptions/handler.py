from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from exceptions.errors import AppException

async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "error_code": "validation_error",
            "details": [error["msg"] for error in exc.errors()]
        },
    )

async def app_exception_handler(_: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.__class__.__name__,
            "details": exc.detail
        },
    )