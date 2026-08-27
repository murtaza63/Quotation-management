from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class QuotationBase(BaseModel):
    customer_id: int
    quotation_date: date
    valid_until: date
    status: str = "draft"
    vat_percentage: Decimal = Decimal("5.00")
    notes: str | None = None


class QuotationCreate(QuotationBase):
    pass


class QuotationUpdate(BaseModel):
    customer_id: int | None = None
    quotation_date: date | None = None
    valid_until: date | None = None
    status: str | None = None
    vat_percentage: Decimal | None = None
    notes: str | None = None


class QuotationResponse(QuotationBase):
    id: int
    quotation_number: str
    subtotal: Decimal
    vat_amount: Decimal
    total_amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True
