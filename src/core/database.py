# src/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)


class AsyncDatabase:
    def __init__(self):
        self.engine = None
        self.async_session = None

    async def connect(self):
        """Инициализация подключения к реальной БД"""
        self.engine = create_async_engine(
            str(settings.ASYNC_DATABASE_URL),
            echo=settings.DEBUG,
            pool_pre_ping=True
        )
        self.async_session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        logger.info("Database connection established")

    def get_session(self) -> AsyncSession:
        """Возвращает реальную сессию БД"""
        return self.async_session()

adb = AsyncDatabase()
