from decimal import Decimal

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from app.db.database import Base


class QuotationItem(Base):
    __tablename__ = "quotation_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=False,
    )

    description = Column(
        String,
        nullable=False,
    )

    quantity = Column(
        Numeric(12, 2),
        nullable=False,
    )

    unit = Column(
        String,
        nullable=False,
    )

    unit_price = Column(
        Numeric(12, 2),
        nullable=False,
    )

    total = Column(
        Numeric(14, 2),
        nullable=False,
        default=Decimal("0.00"),
    )
