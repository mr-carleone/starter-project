# src/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.mocks import MockAsyncSession
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)


class AsyncDatabase:
    def __init__(self):
        self.engine = None
        self.async_session = None

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
            except Exception as e:
                logger.error(f"Database connection error: {e}")
                self.is_connected = False
        else:
            self.is_connected = False

    def get_session(self) -> AsyncSession:
        if self.is_connected:
            return self.async_session()
        return MockAsyncSession()

adb = AsyncDatabase()
