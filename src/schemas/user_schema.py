# src/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID
from typing import Optional
import re


class RoleBase(BaseModel):
    name: str = Field(..., max_length=50, example="ROLE_NAME")

    class Config:
        from_attributes = True
        json_schema_extra = {"example": {"name": "ROLE_NAME"}}


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: UUID

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "name": "ROLE_NAME",
            }
        }


class UserBase(BaseModel):
    username: str = Field(..., max_length=50, example="johndoe")
    email: EmailStr = Field(..., max_length=100, example="user@example.com")
    phone: str = Field(..., max_length=20, example="+1234567890")
    is_active: bool = Field(..., example=True)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not re.match(r"^\+?[1-9]\d{7,14}$", v):
            raise ValueError("Invalid phone number format")
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50, example="strongpassword123")
    role_id: UUID = Field(..., example="3fa85f64-5717-4562-b3fc-2c963f66afa6")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50, example="new_username")
    email: Optional[EmailStr] = Field(None, max_length=100, example="new@example.com")
    phone: Optional[str] = Field(None, max_length=20, example="+9876543210")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if v and not re.match(r"^\+?[1-9]\d{7,14}$", v):
            raise ValueError("Invalid phone number format")
        return v


class UserInDB(UserBase):
    id: UUID
    is_active: bool
    role: RoleBase

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "username": "johndoe",
                "email": "user@example.com",
                "phone": "+1234567890",
                "is_active": True,
                "role": {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "name": "ADMIN"},
            }
        }


class UserListResponse(BaseModel):
    users: list[UserInDB]
    count: int = Field(..., example=5)


class DeleteResponse(BaseModel):
    status: str = Field(..., example="success")
    message: str = Field(..., example="User deleted successfully")
