from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.database import Base, engine

import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quotation Management API", version="1.0.0")

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "API Running"}
