from sqlalchemy.orm import Session

from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.core.exceptions import CompanyNameAlreadyExistsException

from app.core.logger import logger


class CustomerService:

    @staticmethod
    def create_customer(db: Session, customer: CustomerCreate):
        logger.info("Creating Customer: %s", customer.company_name)

        existing = CustomerRepository.get_by_company(db, customer.company_name)

        if existing:
            logger.warning("Customer already exists: %s", customer.company_name)
            raise CompanyNameAlreadyExistsException(customer.company_name)
        created_customer = CustomerRepository.create(db, customer)

        logger.info("Customer created successfully. ID=%s", created_customer.id)

        return created_customer

    @staticmethod
    def get_customers(db, skip: int = 0, limit: int = 20):
        return CustomerRepository.get_all(db, skip, limit)

    @staticmethod
    def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
        return CustomerRepository.update(db, customer_id, customer)

    @staticmethod
    def delete_customer(db: Session, customer_id: int):
        return CustomerRepository.delete(db, customer_id)

    @staticmethod
    def get_customer(db: Session, customer_id: int):
        return CustomerRepository.get_by_id(db, customer_id)
