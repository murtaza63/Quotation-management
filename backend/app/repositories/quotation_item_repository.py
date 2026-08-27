from sqlalchemy.orm import Session

from app.models.quotation_item import QuotationItem


class QuotationItemRepository:

    @staticmethod
    def create(
        db: Session,
        quotation_item_data: dict,
    ):
        db_item = QuotationItem(**quotation_item_data)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item

    @staticmethod
    def get_all_by_quotation(
        db: Session,
        quotation_id: int,
    ):
        return (
            db.query(QuotationItem)
            .filter(QuotationItem.quotation_id == quotation_id)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        item_id: int,
    ):
        return db.query(QuotationItem).filter(QuotationItem.id == item_id).first()

    @staticmethod
    def update(
        db: Session,
        item_id: int,
        item_data: dict,
    ):
        db_item = QuotationItemRepository.get_by_id(
            db,
            item_id,
        )

        if not db_item:
            return None

        for key, value in item_data.items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)

        return db_item

    @staticmethod
    def delete(
        db: Session,
        item_id: int,
    ):
        db_item = QuotationItemRepository.get_by_id(
            db,
            item_id,
        )

        if not db_item:
            return False

        db.delete(db_item)
        db.commit()

        return True
