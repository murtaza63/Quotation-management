from sqlalchemy.orm import Session, joinedload

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
        customer_id: int | None = None,
        status: str | None = None,
        quotation_number: str | None = None,
    ):
        query = db.query(Quotation)
        if customer_id is not None:
            query = query.filter(Quotation.customer_id == customer_id)
        if status is not None:
            query = query.filter(Quotation.status == status)
        if quotation_number is not None:
            query = query.filter(
                Quotation.quotation_number.ilike(f"%{quotation_number}%")
            )
        total = query.count()

        items = query.order_by(Quotation.id.desc()).offset(skip).limit(limit).all()

        return items, total

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

    @staticmethod
    def get_detail(
        db: Session,
        quotation_id: int,
    ):
        return (
            db.query(Quotation)
            .options(
                joinedload(Quotation.customer),
                joinedload(Quotation.items),
            )
            .filter(Quotation.id == quotation_id)
            .first()
        )
