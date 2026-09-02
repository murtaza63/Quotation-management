from sqlalchemy.orm import Session

from app.models.qoutation import Quotation
from app.repositories.quotation_repository import QuotationRepository
from app.repositories.customer_repository import CustomerRepository
from app.schemas.quotation import QuotationCreate, QuotationUpdate
from app.services.quotaton_item_service import QuotationItemService
from app.core.logger import logger


class QuotationService:

    @staticmethod
    def create_quotation(
        db: Session,
        quotation: QuotationCreate,
    ):
        logger.info(
            "Creating quotation for customer ID: %s",
            quotation.customer_id,
        )

        customer = CustomerRepository.get_by_id(
            db,
            quotation.customer_id,
        )

        if not customer:
            raise ValueError("Customer not found")

        quotation_number = QuotationService.generate_quotation_number(db)

        quotation_data = quotation.model_dump()

        quotation_data.update(
            {
                "quotation_number": quotation_number,
                "subtotal": 0,
                "vat_amount": 0,
                "total_amount": 0,
            }
        )

        created_quotation = QuotationRepository.create(
            db,
            quotation_data,
        )

        logger.info(
            "Quotation created successfully. ID=%s",
            created_quotation.id,
        )

        return created_quotation

    @staticmethod
    def generate_quotation_number(db: Session):
        count = db.query(Quotation).count()

        return f"QT-2026-{count + 1:04d}"

    @staticmethod
    def get_quotations(
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ):
        return QuotationRepository.get_all(
            db,
            skip,
            limit,
        )

    @staticmethod
    def get_quotation(
        db: Session,
        quotation_id: int,
    ):
        return QuotationRepository.get_by_id(
            db,
            quotation_id,
        )

    @staticmethod
    def update_quotation(
        db: Session,
        quotation_id: int,
        quotation: QuotationUpdate,
    ):
        updated_quotation = QuotationRepository.update(
            db,
            quotation_id,
            quotation,
        )
        if not updated_quotation:
            return None
        # Recalculate subtotal, vat_amount, and total_amount based on the updated items
        QuotationItemService.recalculate_quotation_totals(db, updated_quotation.id)

        return QuotationRepository.get_by_id(
            db,
            quotation_id,
        )

    @staticmethod
    def delete_quotation(
        db: Session,
        quotation_id: int,
    ):
        return QuotationRepository.delete(
            db,
            quotation_id,
        )

    @staticmethod
    def get_quotation_detail(
        db: Session,
        quotation_id: int,
    ):
        return QuotationRepository.get_detail(
            db,
            quotation_id,
        )
