from sqlalchemy.orm import Session

from app.models.qoutation import Quotation
from app.schemas.quotation import QuotationUpdate


class QuotationRepository:

    @staticmethod
    def create(
        db: Session,
        quotation_data: dict,
    ):
        db_quotation = Quotation(**quotation_data)

        db.add(db_quotation)
        db.commit()
        db.refresh(db_quotation)

        return db_quotation

    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 20,
    ):
        return db.query(Quotation).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(
        db: Session,
        quotation_id: int,
    ):
        return db.query(Quotation).filter(Quotation.id == quotation_id).first()

    @staticmethod
    def get_by_number(
        db: Session,
        quotation_number: str,
    ):
        return (
            db.query(Quotation)
            .filter(Quotation.quotation_number == quotation_number)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        quotation_id: int,
        quotation: QuotationUpdate,
    ):
        db_quotation = QuotationRepository.get_by_id(
            db,
            quotation_id,
        )

        if not db_quotation:
            return None

        for key, value in quotation.model_dump(exclude_unset=True).items():
            setattr(
                db_quotation,
                key,
                value,
            )

        db.commit()
        db.refresh(db_quotation)

        return db_quotation

    @staticmethod
    def delete(
        db: Session,
        quotation_id: int,
    ):
        db_quotation = QuotationRepository.get_by_id(
            db,
            quotation_id,
        )

        if not db_quotation:
            return False

        db.delete(db_quotation)
        db.commit()

        return True
