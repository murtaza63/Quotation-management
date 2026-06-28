from sqlalchemy.orm import Session

from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:

    @staticmethod
    def create_customer(db: Session, customer: CustomerCreate):
        return CustomerRepository.create(db, customer)

    @staticmethod
    def get_customers(db: Session):
        return CustomerRepository.get_all(db)

    @staticmethod
    def get_customer(db: Session, customer_id: int):
        return CustomerRepository.get_by_id(db, customer_id)

    @staticmethod
    def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
        return CustomerRepository.update(db, customer_id, customer)

    @staticmethod
    def delete_customer(db: Session, customer_id: int):
        return CustomerRepository.delete(db, customer_id)
