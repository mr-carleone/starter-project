# src/core/mocks.py
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

class MockAsyncSession(AsyncSession):
    def __init__(self):
        super().__init__(bind=AsyncMock())
        self.commit = AsyncMock()
        self.rollback = AsyncMock()
        self.execute = AsyncMock()
        self.close = AsyncMock()
