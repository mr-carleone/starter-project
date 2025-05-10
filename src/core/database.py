# src/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)


class AsyncDatabase:
    def __init__(self):
        self.engine = None
        self.async_session = None
        self.is_connected = False

    async def connect(self):
        if settings.DB_MODE == "real":
            try:
                self.engine = create_async_engine(
                    settings.ASYNC_DATABASE_URL, echo=settings.DEBUG
                )
                self.async_session = async_sessionmaker(
                    self.engine, expire_on_commit=False, class_=AsyncSession
                )
                self.is_connected = True
                logger.info("Async database connected")
            except Exception as e:
                logger.error(f"Database connection error: {e}")
                self.is_connected = False
        else:
            logger.info("Using async mock database")
            self.is_connected = False

    def get_session(self) -> AsyncSession:
        if self.is_connected:
            return self.async_session()
        return MockAsyncSession()


class MockAsyncSession:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def execute(self, *args, **kwargs):
        logger.info(f"Mock async execute: {args[0]}")
        return None

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def close(self):
        pass


adb = AsyncDatabase()
