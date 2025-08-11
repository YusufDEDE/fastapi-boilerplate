import asyncio

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import router as api_router
from app.core.database import AsyncSessionLocal
from app.core.middleware.basic_auth import BasicAuthMiddleware
from app.seeder.example_seed import egypt_seed_data

from app.services.external.email_send_client import EmailSendClient
from app.services.internal.example_listener import ExampleListener
from app.web import router as web_router
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    integrity_exception_handler,
    uuid_parse_error_handler,
    generic_exception_handler,
)

_app_name = settings.APP_NAME

app = FastAPI(
    title=_app_name,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="FastAPI - fastapi-boilerplate",
    docs_url=f"/api-docs",  # Custom Swagger path
    redoc_url=None,  # ReDoc disabled
    # openapi_url=f"/openapi.json"  # Custom OpenAPI spec path
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE vs.
    allow_headers=["*"],  # Authorization, Content-Type vs.
)

app.add_middleware(BasicAuthMiddleware)

app.include_router(api_router)
app.include_router(web_router)

# Register handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(ValueError, uuid_parse_error_handler)  # For UUID casting
app.add_exception_handler(Exception, generic_exception_handler)  # Catch-all

# EXTERNAL - Services Initialize Section
_email_client = EmailSendClient(
    smtp_host=settings.EMAIL_HOST,
    smtp_port=settings.EMAIL_PORT,
    username=settings.EMAIL_USERNAME,
    password=settings.EMAIL_PASSWORD,
)

# INTERNAL - Services Initialize Section
_example_listener = ExampleListener()


@app.on_event("startup")
async def on_startup():
    if settings.IS_SEED_DATA_EXEC:
        async with AsyncSessionLocal() as db:
            await egypt_seed_data(db=db)

    asyncio.create_task(_example_listener.start_listener())
