from decimal import Decimal

from pydantic import BaseModel, Field


class QuotationItemBase(BaseModel):
    description: str
    quantity: Decimal = Field(
        gt=Decimal("0"),
        max_digits=12,
        decimal_places=2,
    )
    unit: str
    unit_price: Decimal = Field(
        gt=Decimal("0"),
        max_digits=12,
        decimal_places=2,
    )


class QuotationItemCreate(QuotationItemBase):
    pass


class QuotationItemUpdate(BaseModel):
    description: str | None = None
    quantity: Decimal | None = Field(
        default=None,
        gt=Decimal("0"),
        max_digits=12,
        decimal_places=2,
    )
    unit: str | None = None
    unit_price: Decimal | None = Field(
        default=None,
        gt=Decimal("0"),
        max_digits=12,
        decimal_places=2,
    )


class QuotationItemResponse(QuotationItemBase):
    id: int
    quotation_id: int
    total: Decimal

    class Config:
        from_attributes = True
