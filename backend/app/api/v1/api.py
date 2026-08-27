from fastapi import APIRouter

from app.api.v1.endpoints import (
    health,
    customers,
    auth,
    quotations,
    quotation_items,
)

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(health.router)

api_router.include_router(
    customers.router,
    prefix="/customers",
    tags=["Customers"],
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    quotations.router,
    prefix="/quotations",
    tags=["Quotations"],
)

api_router.include_router(quotation_items.router)
