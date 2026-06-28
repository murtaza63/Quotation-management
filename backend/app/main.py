from fastapi import FastAPI

from app.db.database import engine, Base

import app.models

app = FastAPI(title="Quotation Management API")

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API Running"}
