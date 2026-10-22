from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class CustomerBase(BaseModel):
    company_name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
