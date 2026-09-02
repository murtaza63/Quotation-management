from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Numeric
from app.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    quotation_number = Column(String, unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    quotation_date = Column(Date, nullable=False)
    valid_until = Column(Date, nullable=False)
    status = Column(String, default="draft", nullable=False)
    subtotal = Column(Numeric(10, 2), default=0, nullable=False)
    vat_percentage = Column(Numeric(5, 2), nullable=False)
    vat_amount = Column(Numeric(12, 2), nullable=False)
    total_amount = Column(Numeric(12, 2), default=0, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    customer = relationship("Customer", back_populates="quotations")

    items = relationship(
        "QuotationItem",
        back_populates="quotation",
    )
