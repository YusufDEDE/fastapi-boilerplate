from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
import uuid
import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )


async def integrity_exception_handler(request: Request, exc: IntegrityError):
    logger.error(f"Integrity error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": "Integrity constraint failed. Check unique fields or null values."}
    )


async def uuid_parse_error_handler(request: Request, exc: ValueError):
    # Genelde UUID parse edilirken ValueError fırlatır
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid UUID format"}
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error occurred")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )
