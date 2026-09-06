from datetime import date, datetime
from decimal import Decimal
from app.schemas.customer import CustomerResponse
from app.schemas.quotation_item import QuotationItemResponse
from enum import Enum
from pydantic import BaseModel, Field, model_validator


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
        default=Decimal("0.00"),
        ge=Decimal("0.00"),
        le=Decimal("100.00"),
        max_digits=5,
        decimal_places=2,
    )
    notes: str | None = None


class QuotationCreate(QuotationBase):
    @model_validator(mode="before")
    @classmethod
    def validate_dates(cls, values):
        if (
            "quotation_date" in values
            and "valid_until" in values
            and values["valid_until"] < values["quotation_date"]
        ):
            raise ValueError("valid_until cannot be earlier than quotation_date")
        return values


class QuotationUpdate(BaseModel):
    customer_id: int | None = None
    quotation_date: date | None = None
    valid_until: date | None = None
    status: QuotationStatus | None = None
    vat_percentage: Decimal | None = Field(
        default=None,
        ge=Decimal("0.00"),
        le=Decimal("100.00"),
        max_digits=5,
        decimal_places=2,
    )

    @model_validator(mode="before")
    @classmethod
    def validate_dates(cls, values):
        if not isinstance(values, dict):
            return values
        quotation_date = values.get("quotation_date")
        valid_until = values.get("valid_until")

        if (
            quotation_date is not None
            and valid_until is not None
            and valid_until < quotation_date
        ):
            raise ValueError("valid_until cannot be earlier than quotation_date")

        return values


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


class QuotationListResponse(BaseModel):
    items: list[QuotationResponse]
    total: int
    skip: int
    limit: int
