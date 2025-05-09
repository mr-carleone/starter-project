# src/services/base_service.py
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError


class BaseService(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @classmethod
    @abstractmethod
    async def create(cls, session: AsyncSession):
        pass

    async def commit(self):
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.rollback()
            raise self._handle_db_error(e)

    async def rollback(self):
        await self.session.rollback()

    @staticmethod
    def _handle_db_error(error: SQLAlchemyError) -> Exception:
        error_type = type(error).__name__
        return RuntimeError(f"Database error [{error_type}]: {str(error)}")
