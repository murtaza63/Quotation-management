from decimal import Decimal

from pydantic import BaseModel


class QuotationItemBase(BaseModel):
    description: str
    quantity: Decimal
    unit: str
    unit_price: Decimal


class QuotationItemCreate(QuotationItemBase):
    pass


class QuotationItemUpdate(BaseModel):
    description: str | None = None
    quantity: Decimal | None = None
    unit: str | None = None
    unit_price: Decimal | None = None


class QuotationItemResponse(QuotationItemBase):
    id: int
    quotation_id: int
    total: Decimal

    class Config:
        from_attributes = True
