# src/core/dependencies.py
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import adb
from typing import AsyncGenerator


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with adb.get_session() as session:
        yield session
