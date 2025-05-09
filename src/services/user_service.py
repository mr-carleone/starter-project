# src/services/user_service.py
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.base_service import BaseService
from src.repositories.user_repository import AsyncUserRepository
from src.services.role_service import RoleService
from src.schemas.user_schema import UserCreate, UserInDB
from src.core.exceptions import NotFoundError
from uuid import UUID


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = AsyncUserRepository(session)
        self.role_service = RoleService(session)

    @classmethod
    async def create(cls, session: AsyncSession):
        return cls(session)

    async def role_exists(self, role_id: UUID) -> bool:
        return await self.repo.role_exists(role_id)

    async def get_user_by_username(self, username: str) -> UserInDB:
        user = await self.repo.get_user_by_username(username)
        if not user:
            raise NotFoundError(f"User {username} not found")
        return UserInDB.model_validate(user)

    async def delete_user(self, user_id: UUID) -> None:
        await self.repo.delete_user(user_id)
        await self.commit()

    async def create_user_without_commit(self, user_data: UserCreate) -> UserInDB:
        try:
            await self.role_service.get_role_by_id(user_data.role_id)
            user = await self.repo.create_user(user_data, user_data.role_id)
            return UserInDB.model_validate(user)
        except IntegrityError as e:
            error_msg = str(e.orig).lower()
            field = next(
                (f for f in ["username", "email", "phone"] if f in error_msg), "unknown"
            )
            raise ValueError(f"{field.capitalize()} already exists")

    async def create_user(self, user_data: UserCreate) -> UserInDB:
        try:
            # Проверка роли через сервис
            await self.role_service.get_role_by_id(user_data.role_id)

            # Создание пользователя
            user = await self.repo.create_user(user_data, user_data.role_id)
            await self.commit()
            return user

        except IntegrityError as e:
            await self.rollback()
            error_msg = str(e.orig).lower()
            field = next(
                (f for f in ["username", "email", "phone"] if f in error_msg), "unknown"
            )
            raise ValueError(f"{field.capitalize()} already exists")
