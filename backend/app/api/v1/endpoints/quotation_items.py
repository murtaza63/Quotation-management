from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.repositories.quotation_item_repository import QuotationItemRepository
from app.schemas.quotation_item import (
    QuotationItemCreate,
    QuotationItemUpdate,
    QuotationItemResponse,
)
from app.services.quotaton_item_service import QuotationItemService

router = APIRouter(
    tags=["Quotation Items"],
)


@router.post(
    "/quotations/{quotation_id}/items",
    response_model=QuotationItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_quotation_item(
    quotation_id: int,
    item: QuotationItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    created_item = QuotationItemService.create_item(
        db,
        quotation_id,
        item,
    )

    if not created_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found",
        )

    return created_item


@router.get(
    "/quotations/{quotation_id}/items",
    response_model=list[QuotationItemResponse],
)
def get_quotation_items(
    quotation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return QuotationItemRepository.get_all_by_quotation(
        db,
        quotation_id,
    )


@router.put(
    "/quotation-items/{item_id}",
    response_model=QuotationItemResponse,
)
def update_quotation_item(
    item_id: int,
    item: QuotationItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated_item = QuotationItemService.update_item(
        db,
        item_id,
        item,
    )

    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation item not found",
        )

    return updated_item


@router.delete(
    "/quotation-items/{item_id}",
)
def delete_quotation_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    deleted = QuotationItemService.delete_item(
        db,
        item_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation item not found",
        )

    return {"message": "Quotation item deleted successfully"}
