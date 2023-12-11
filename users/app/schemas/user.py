from typing import Optional

from pydantic import BaseModel, EmailStr, UUID4, validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "password": "strongpassword",
            }
        }

    @validator("password")
    def validate_password(cls, v):
        if len(v) <= 6:
            raise ValueError("Password must be more than 6 characters")
        return v


class UserOut(UserBase):
    user_id: UUID4

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserUpdateDB(UserBase):
    password: str
