# src/services/auth_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import create_access_token
from src.repositories.user_repository import AsyncUserRepository
from src.schemas.auth_schema import TokenResponse
from src.services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.user_repo = AsyncUserRepository(session)
        self._current_user = None

    @classmethod
    async def create(cls, session: AsyncSession):
        return cls(session)

    @property
    async def current_user(self):
        """Ленивая загрузка текущего пользователя"""
        if self._current_user is None:
            raise ValueError("User not authenticated")
        return self._current_user

    async def authenticate(self, username: str, password: str) -> TokenResponse:
        """Основная логика аутентификации"""
        user = await self.user_repo.authenticate_user(username, password)
        if not user:
            raise ValueError("Invalid credentials")

        self._current_user = user
        return {"access_token": create_access_token(user.id), "token_type": "bearer"}
