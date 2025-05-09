# src/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


class RoleBase(BaseModel):
    id: UUID
    name: str = Field(..., max_length=50)

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=100)
    phone: str = Field(..., max_length=20)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=50)
    role_id: UUID = Field(..., description="ID роли пользователя")


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8, max_length=50)


class UserInDB(UserBase):
    id: UUID
    role_id: UUID
    role: RoleBase  # Добавляем вложенную схему роли

    class Config:
        from_attributes = True
