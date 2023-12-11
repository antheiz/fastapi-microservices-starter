from typing import Optional

from pydantic import BaseModel, EmailStr, UUID4, validator


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    gender: str
    phone: str
    date_of_birth: str
    photo: Optional[str] = None


class CustomerOut(CustomerBase):
    pass

    class Config:
        from_attributes = True


class CustomerUpdate(CustomerBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    photo: Optional[str] = None
