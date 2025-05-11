# tests/mocks/database.py
from unittest.mock import AsyncMock, MagicMock

class MockAsyncSession:
    def __init__(self):
        self.execute = AsyncMock()
        self.commit = AsyncMock()
        self.rollback = AsyncMock()
        self.close = AsyncMock()
        self.scalar = AsyncMock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

class MockDatabase:
    def __init__(self):
        self.async_session = MagicMock(return_value=MockAsyncSession())
        self.engine = MagicMock()
