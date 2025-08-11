from fastapi import APIRouter

from app.api.v1.routes.example import example_router

router = APIRouter()

API_PREFIX = "/api/v1"
# v1/api/
router.include_router(example_router, prefix=f"{API_PREFIX}")
