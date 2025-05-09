# src/services/user_service.py
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.base_service import BaseService
from src.repositories.user_repository import AsyncUserRepository
from src.services.role_service import RoleService
from src.schemas.user_schema import UserCreate, UserInDB


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.repo = AsyncUserRepository(session)
        self.role_service = RoleService(session)

    @classmethod
    async def create(cls, session: AsyncSession):
        return cls(session)

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
