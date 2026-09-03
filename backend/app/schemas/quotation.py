from datetime import date, datetime
from decimal import Decimal
from app.schemas.customer import CustomerResponse
from app.schemas.quotation_item import QuotationItemResponse
from enum import Enum
from pydantic import BaseModel, Field


class QuotationStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    APPROVED = "approved"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class QuotationBase(BaseModel):
    customer_id: int
    quotation_date: date
    valid_until: date
    status: QuotationStatus = QuotationStatus.DRAFT
    vat_percentage: Decimal = Field(
        default=Decimal("0.00"), max_digits=5, decimal_places=2
    )
    notes: str | None = None


class QuotationCreate(QuotationBase):
    pass


class QuotationUpdate(BaseModel):
    customer_id: int | None = None
    quotation_date: date | None = None
    valid_until: date | None = None
    status: QuotationStatus | None = None
    vat_percentage: Decimal | None = None
    notes: str | None = None


class QuotationResponse(QuotationBase):
    id: int
    quotation_number: str
    subtotal: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    vat_amount: Decimal = Field(
        default=Decimal("0.00"), max_digits=12, decimal_places=2
    )
    total_amount: Decimal = Field(
        default=Decimal("0.00"), max_digits=12, decimal_places=2
    )
    created_at: datetime

    class Config:
        from_attributes = True


class QuotationDetailResponse(QuotationResponse):
    customer: CustomerResponse
    items: list[QuotationItemResponse]
