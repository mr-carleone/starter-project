# src/services/healthcheck_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.core.config import settings
from src.services.base_service import BaseService


class HealthcheckService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    @classmethod
    async def create(cls, session: AsyncSession):
        return cls(session)

    @property
    def db_mode(self) -> str:
        """Текущий режим работы с БД (только для чтения)"""
        return settings.DB_MODE

    async def perform_db_check(self) -> dict:
        """Основной метод проверки соединения с БД"""
        if self.db_mode == "mock":
            return {"status": "OK", "db_mode": "mock"}

        try:
            await self.session.execute(text("SELECT 1"))
            return {"status": "OK", "db_connection": "success"}
        except Exception as e:
            raise RuntimeError(f"Database connection failed: {str(e)}")
