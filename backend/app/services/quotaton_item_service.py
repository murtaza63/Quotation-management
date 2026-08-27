from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.quotation_repository import QuotationRepository
from app.repositories.quotation_item_repository import QuotationItemRepository
from app.schemas.quotation_item import (
    QuotationItemCreate,
    QuotationItemUpdate,
)


class QuotationItemService:

    @staticmethod
    def calculate_item_total(
        quantity: Decimal,
        unit_price: Decimal,
    ) -> Decimal:
        return quantity * unit_price

    @staticmethod
    def create_item(
        db: Session,
        quotation_id: int,
        item: QuotationItemCreate,
    ):
        quotation = QuotationRepository.get_by_id(
            db,
            quotation_id,
        )

        if not quotation:
            return None

        total = QuotationItemService.calculate_item_total(
            item.quantity,
            item.unit_price,
        )

        item_data = item.model_dump()

        item_data["quotation_id"] = quotation_id
        item_data["total"] = total

        created_item = QuotationItemRepository.create(
            db,
            item_data,
        )

        QuotationItemService.recalculate_quotation_totals(
            db,
            quotation_id,
        )

        return created_item

    @staticmethod
    def recalculate_quotation_totals(
        db: Session,
        quotation_id: int,
    ):
        quotation = QuotationRepository.get_by_id(
            db,
            quotation_id,
        )

        if not quotation:
            return None

        items = QuotationItemRepository.get_all_by_quotation(
            db,
            quotation_id,
        )

        subtotal = sum(
            (item.total for item in items),
            Decimal("0.00"),
        )

        vat_amount = (subtotal * quotation.vat_percentage) / Decimal("100")

        total_amount = subtotal + vat_amount

        quotation.subtotal = subtotal
        quotation.vat_amount = vat_amount
        quotation.total_amount = total_amount

        db.commit()
        db.refresh(quotation)

        return quotation

    @staticmethod
    def update_item(
        db: Session,
        item_id: int,
        item: QuotationItemUpdate,
    ):
        db_item = QuotationItemRepository.get_by_id(
            db,
            item_id,
        )

        if not db_item:
            return None

        item_data = item.model_dump(
            exclude_unset=True,
        )

        quantity = item_data.get(
            "quantity",
            db_item.quantity,
        )

        unit_price = item_data.get(
            "unit_price",
            db_item.unit_price,
        )

        item_data["total"] = QuotationItemService.calculate_item_total(
            quantity,
            unit_price,
        )

        updated_item = QuotationItemRepository.update(
            db,
            item_id,
            item_data,
        )

        QuotationItemService.recalculate_quotation_totals(
            db,
            updated_item.quotation_id,
        )

        return updated_item

    @staticmethod
    def delete_item(
        db: Session,
        item_id: int,
    ):
        db_item = QuotationItemRepository.get_by_id(
            db,
            item_id,
        )

        if not db_item:
            return False

        quotation_id = db_item.quotation_id

        deleted = QuotationItemRepository.delete(
            db,
            item_id,
        )

        if deleted:
            QuotationItemService.recalculate_quotation_totals(
                db,
                quotation_id,
            )

        return deleted
