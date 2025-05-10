# src/core/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import adb
from typing import AsyncGenerator


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для получения сессии БД"""
    async with adb.get_session() as session:
        yield session
