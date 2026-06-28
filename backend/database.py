import os
from sqlmodel import SQLModel, create_engine, Session

# Replace username, password, and quotation_db with your local PostgreSQL details
# If you used Psycopg 3, use: "postgresql+psycopg://..."
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5432/quotation_db"
)

# echo=True prints SQL queries to the terminal (great for development)
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Creates the database tables based on our SQLModels"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Provides a transactional database session for API endpoints"""
    with Session(engine) as session:
        yield session
