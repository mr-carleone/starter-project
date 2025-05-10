# src/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import settings
from typing import Any
from types import TracebackType
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
                    str(settings.ASYNC_DATABASE_URL),
                    echo=settings.DEBUG,
                    pool_pre_ping=True
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
    """Mock async session for testing purposes."""

    async def __aenter__(self) -> "MockAsyncSession":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> None:
        """Handle context manager exit, ignoring any exceptions."""
        if exc_val:
            logger.debug("Mock session ignored exception: %s", exc_val)

    async def execute(
        self,
        statement: Any,
    ) -> None:
        """Log the executed statement and return mock result."""
        logger.info("Mock async execute: %s", statement)
        return None

    async def commit(self) -> None:
        """Mock commit operation."""
        logger.debug("Mock commit")

    async def rollback(self) -> None:
        """Mock rollback operation."""
        logger.debug("Mock rollback")

    async def close(self) -> None:
        """Mock connection close."""
        logger.debug("Mock connection closed")


adb = AsyncDatabase()
