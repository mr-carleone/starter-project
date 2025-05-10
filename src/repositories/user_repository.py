# src/repositories/user_repository.py
from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from src.core.security import pwd_context

from src.entities.user import User, Role
from src.schemas.user_schema import UserCreate


class AsyncUserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def role_exists(self, role_id: UUID) -> bool:
        result = await self.db.execute(select(Role).filter(Role.id == role_id))
        return result.scalars().first() is not None

    async def get_user_by_username(self, username: str) -> User:
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.get_user_by_username(username)
        if user and pwd_context.verify(password, user.hashed_password):
            return user
        return None

    async def delete_user(self, user_id: UUID) -> bool:
        user = await self.db.get(User, user_id)
        if not user:
            return False
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def create_user(
        self, user_data: UserCreate, role_id: UUID, created_by: str
    ) -> User:
        hashed_password = pwd_context.hash(user_data.password)

        user = User(
            username=user_data.username,
            email=user_data.email,
            phone=user_data.phone,
            hashed_password=hashed_password,
            role_id=role_id,
            is_active=user_data.is_active,
            created_by=created_by,
        )

        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError as e:
            await self.db.rollback()
            if "username" in str(e):
                raise ValueError("Username already exists")
            elif "email" in str(e):
                raise ValueError("Email already exists")
            elif "phone" in str(e):
                raise ValueError("Phone number already exists")
            raise ValueError("Database integrity error")

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def update_user(
        self, user_id: UUID, update_values: dict, updated_by: str
    ) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.updated_by = updated_by

        # Обновляем только разрешенные поля
        allowed_fields = {"username", "email", "phone", "hashed_password", "role_id"}
        for key, value in update_values.items():
            if key in allowed_fields:
                setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_all_users(self) -> List[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()
