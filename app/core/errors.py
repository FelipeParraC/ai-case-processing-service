from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.logger import get_logger
from app.api.schemas.error_response import ErrorResponse


logger = get_logger("errors")


def http_exception_handler(request: Request, exc: HTTPException):

    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        "http_exception",
        extra={
            "extra": {
                "request_id": request_id,
                "status_code": exc.status_code,
                "detail": exc.detail,
            }
        }
    )

    payload = ErrorResponse(
        request_id=request_id,
        error_code="HTTP_ERROR",
        message=str(exc.detail),
        details={"status_code": exc.status_code},
    ).model_dump()

    return JSONResponse(status_code=exc.status_code, content=payload)


def unhandled_exception_handler(request: Request, exc: Exception):

    request_id = getattr(request.state, "request_id", "unknown")

    logger.error(
        "unhandled_exception",
        extra={"extra": {"request_id": request_id, "error": str(exc)}}
    )

    payload = ErrorResponse(
        request_id=request_id,
        error_code="INTERNAL_ERROR",
        message="Unexpected error occurred",
    ).model_dump()

    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=payload
    )
