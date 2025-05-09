# src/core/unit_of_work.py
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.role_repository import AsyncRoleRepository
from src.repositories.user_repository import AsyncUserRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.role_repo = AsyncRoleRepository(session)
        self.user_repo = AsyncUserRepository(session)
        # Добавьте другие репозитории по мере необходимости

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
