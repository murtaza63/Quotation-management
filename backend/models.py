from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Quotation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_name: str
    property_address: str
    square_footage: float
    estimated_cost: float
    hazard_level: str = Field(default="Low")  # e.g., Low, Medium, High (Asbestos)
    status: str = Field(default="Draft")  # e.g., Draft, Sent, Approved
    created_at: datetime = Field(default_factory=datetime.utcnow)
