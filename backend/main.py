from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Depends
from database import create_db_and_tables, get_session
from models import Quotation

try:
    from sqlmodel import Session, select
except ImportError:  # pragma: no cover
    from sqlalchemy.orm import Session
    from sqlalchemy import select


# Automatically create tables when the backend app starts up
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


def _execute_statement(session: Session, statement: Any):
    try:
        return session.exec(statement)
    except AttributeError:
        return session.execute(statement)


# Endpoint to create a new demolition quote
@app.post("/api/quotations/", response_model=Quotation)
def create_quotation(quotation: Quotation, session: Session = Depends(get_session)):
    session.add(quotation)
    session.commit()
    session.refresh(quotation)
    return quotation


# Endpoint to fetch all quotes
@app.get("/api/quotations/", response_model=list[Quotation])
def read_quotations(session: Session = Depends(get_session)):
    statement = select(Quotation)
    result = _execute_statement(session, statement)
    return result.scalars().all() if hasattr(result, "scalars") else result.all()
