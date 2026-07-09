from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.exceptions import CompanyNameAlreadyExistsException

app = FastAPI(title="Quotation Management API", version="1.0.0")

app.include_router(api_router)


@app.exception_handler(CompanyNameAlreadyExistsException)
async def company_exists_exception_handler(
    request: Request,
    exc: CompanyNameAlreadyExistsException,
):
    return JSONResponse(
        status_code=409,
        content={"detail": f"Company '{exc.company_name}' already exists."},
    )


@app.get("/")
def root():
    return {"message": "API Running"}
