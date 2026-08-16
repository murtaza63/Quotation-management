from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.api.v1.endpoints import customers, auth

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(customers.router)

api_router.include_router(customers.router, prefix="/customers", tags=["customers"])


api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
