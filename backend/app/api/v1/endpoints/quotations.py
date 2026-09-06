from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas.quotation import (
    QuotationCreate,
    QuotationUpdate,
    QuotationResponse,
    QuotationDetailResponse,
    QuotationListResponse,
)
from app.services.quotation_service import QuotationService

router = APIRouter()


@router.post(
    "",
    response_model=QuotationResponse,
)
def create_quotation(
    quotation: QuotationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return QuotationService.create_quotation(
        db,
        quotation,
    )


@router.get(
    "/",
    response_model=QuotationListResponse,
)
def get_quotations(
    skip: int = 0,
    limit: int = 20,
    customer_id: int | None = None,
    status: str | None = None,
    quotation_number: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return QuotationService.get_quotations(
        db=db,
        skip=skip,
        limit=limit,
        customer_id=customer_id,
        status=status,
        quotation_number=quotation_number,
    )


@router.get(
    "/{quotation_id}/details",
    response_model=QuotationDetailResponse,
)
def get_quotation_detail(
    quotation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    quotation = QuotationService.get_quotation_detail(
        db,
        quotation_id,
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    return quotation


@router.get(
    "/{quotation_id}",
    response_model=QuotationResponse,
)
def get_quotation(
    quotation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    quotation = QuotationService.get_quotation(
        db,
        quotation_id,
    )

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    return quotation


@router.put(
    "/{quotation_id}",
    response_model=QuotationResponse,
)
def update_quotation(
    quotation_id: int,
    quotation: QuotationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    updated = QuotationService.update_quotation(
        db,
        quotation_id,
        quotation,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    return updated


@router.delete(
    "/{quotation_id}",
)
def delete_quotation(
    quotation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    deleted = QuotationService.delete_quotation(
        db,
        quotation_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    return {"message": "Quotation deleted successfully"}
