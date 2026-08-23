from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services.customer_service import CustomerService
from app.repositories.customer_repository import CustomerRepository

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return CustomerService.create_customer(db, customer)


@router.get("/")
def get_customers(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return CustomerService.get_customers(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerService.get_customer(db, customer_id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)
):
    updated = CustomerService.update_customer(db, customer_id, customer)

    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")

    return updated


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    deleted = CustomerService.delete_customer(db, customer_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"message": "Customer deleted successfully"}


@router.get("/search")
def search_customer(company_name: str, db: Session = Depends(get_db)):
    return CustomerRepository.search(db, company_name)
